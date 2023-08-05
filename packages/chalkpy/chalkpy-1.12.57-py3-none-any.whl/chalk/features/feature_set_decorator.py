import ast
import copy
import functools
import inspect
from itertools import islice
import re
import textwrap
import threading
import types
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Type, TypeVar, Union, cast, overload

import sys

from chalk.features._class_property import classproperty, classproperty_support
from chalk.features.feature_field import Feature, _VersionInfo
from chalk.features.feature_set import Features, FeatureSetBase
from chalk.features.feature_time import feature_time
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.tag import Tags
from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.streams import Windowed
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import Duration, timedelta_to_duration
from chalk.utils.metaprogramming import MISSING, create_fn, field_assign, set_new_attribute
from chalk.utils.string import removeprefix, to_snake_case

T = TypeVar("T")

__all__ = ["features"]

GENERATED_OBSERVED_AT_NAME = "__chalk_observed_at__"


@overload
def features(
    *,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: bool = ...,
    max_staleness: Optional[Duration] = ...,
    name: Optional[str] = None,
) -> Callable[[Type[T]], Type[T]]:
    ...


@overload
def features(cls: Type[T]) -> Type[T]:
    ...


def features(
    cls: Optional[Type[T]] = None,
    *,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: Optional[bool] = None,
    max_staleness: Optional[Duration] = ...,
    name: Optional[str] = None,
) -> Union[Callable[[Type[T]], Type[T]], Type[T]]:
    """Chalk lets you spell our your features directly in Python.

    Features are namespaced to a `FeatureSet`.
    To create a new `FeatureSet`, apply the `@features`
    decorator to a Python class with typed attributes.
    A `FeatureSet` is constructed and functions much like
    Python's own `dataclass`.

    Parameters
    ----------
    owner
        The individual or team responsible for these features.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.
    tags
        Added metadata for features for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
    etl_offline_to_online
        When `True`, Chalk copies this feature into the online environment
        when it is computed in offline resolvers.
        Setting `etl_offline_to_online` on a feature class assigns it to all features on the
        class which do not explicitly specify `etl_offline_to_online`.
    max_staleness
        When a feature is expensive or slow to compute, you may wish to cache its value.
        Chalk uses the terminology "maximum staleness" to describe how recently a feature
        value needs to have been computed to be returned without re-running a resolver.
        Assigning a `max_staleness` to the feature class assigns it to all features on the
        class which do not explicitly specify a `max_staleness` value of their own.

    Other Parameters
    ----------------
    cls
        The decorated class. You shouldn't need to pass this argument.
    name
        The name for the feature. By default, the name of a feature is
        taken from the name of the attribute on the class, prefixed with
        the camel-cased name of the class. Note that if you provide an
        explicit name, the name of the feature class will still be
        prepended with a `.`. You may also override the name of the

    Examples
    --------
    >>> @features(owner="andy@chalk.ai", max_staleness="30m")
    ... class User:
    ...     id: str
    ...     name: str | None
    """

    def wrap(c: Type[T]) -> Type[T]:
        namespace = name or to_snake_case(c.__name__)
        if name is not None and re.sub(r"[^a-z_0-9]", "", namespace) != namespace:
            raise ValueError(
                (
                    f"Namespace must be composed of lower-case alpha-numeric characters and '_'. Provided namespace "
                    f"'{namespace}' for class '{c.__name__}' contains invalid characters."
                )
            )
        if name is not None and len(namespace) == 0:
            raise ValueError(f"Namespace cannot be an empty string, but is for the class '{c.__name__}'.")
        updated_class = _process_class(
            cls=c,
            owner=owner,
            tags=ensure_tuple(tags),
            etl_offline_to_online=etl_offline_to_online,
            max_staleness=timedelta_to_duration(max_staleness)
            if isinstance(max_staleness, timedelta)
            else max_staleness,
            namespace=namespace,
        )
        assert issubclass(updated_class, Features)
        FeatureSetBase.registry[updated_class.__chalk_namespace__] = updated_class
        if FeatureSetBase.hook is not None:
            FeatureSetBase.hook(cast(Features, updated_class))

        return cast(Type[T], updated_class)

    # See if we're being called as @features or @features().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @features without parens.
    return wrap(cls)


def _discover_feature(
    features: Sequence[Feature], name: str, *conditions: Callable[[Feature], bool]
) -> Optional[Feature]:
    for cond in conditions:
        filtered_features = [c for c in features if cond(c)]
        if len(filtered_features) == 1:
            return filtered_features[0]
        if len(filtered_features) > 1:
            assert filtered_features[0].features_cls is not None
            feature_cls_name = filtered_features[0].features_cls.__name__
            raise ValueError(
                f"Multiple {name} features are not supported in {feature_cls_name}: "
                + ", ".join(f"{feature_cls_name}.{x.name}" for x in filtered_features)
            )
    return None


def _init_param(name: str, annotation: Any, _locals: Dict[str, Any]):
    # Return the __init__ parameter string for this field.  For
    # example, the equivalent of 'x:int=3' (except instead of 'int',
    # reference a variable set to int, and instead of '3', reference a
    # variable set to 3).
    annotation_name = f"_type_{name}"
    _locals[annotation_name] = annotation
    return f"{name}:{annotation_name}=MISSING"


def _setattr_fn(bidirectional_alias: Dict[str, str], _globals: Dict[str, Any]):
    return create_fn(
        name="__setattr__",
        args=["self", "key", "value"],
        body=[
            f"alias = {bidirectional_alias}",
            "if key in alias:",
            "    super(self.__class__, self).__setattr__(alias[key], value)",
            "return super(self.__class__, self).__setattr__(key, value)",
        ],
        _globals=_globals,
        _locals={},
        return_type=None,
    )


def _getattribute_fn(_globals: Dict[str, Any]):
    # If calling getattr() on an instance for a feature name,
    # do NOT return a class-level FeatureWrapper.
    # Instead, raise an attribute error

    return create_fn(
        name="__getattribute__",
        args=["self", "attribute_name"],
        body=[
            "o = object.__getattribute__(self, attribute_name)",
            "if isinstance(o, FeatureWrapper):",
            "    raise AttributeError(f'Feature \\'{attribute_name}\\' is not defined on this instance of class \\'{type(self).__name__}\\'')",
            "return o",
        ],
        _globals=_globals,
        _locals={
            "FeatureWrapper": FeatureWrapper,
        },
        return_type=Any,
    )


def _init_fn(
    feature_names_and_annotations: List[Tuple[str, Any]],
    alias_from_to: Mapping[str, str],
    _globals: Dict[str, Any],
):
    _locals = {
        "MISSING": MISSING,
    }
    _init_params = [_init_param(name, annotation, _locals) for (name, annotation) in feature_names_and_annotations]
    _init_params.append(_init_param(GENERATED_OBSERVED_AT_NAME, datetime, _locals))

    # Not using "self" for the self name in case if there is a feature called "self"
    self_name = "__chalk_self__"
    body_lines: List[str] = []
    for from_, to in alias_from_to.items():
        body_lines.extend(
            [
                f"if {from_} is not MISSING and {to} is not MISSING:"
                f"    raise ValueError('The features \\'{from_}\\' and \\'{to}\\' are aliases of each other. Only one can be specified, but both were given.')",
                f"{from_} = {to} if {from_} is MISSING else {from_}",
            ]
        )
    body_lines.extend([field_assign(name, name, self_name) for (name, _) in feature_names_and_annotations])

    # Check to see whether the GENERATED_OBSERVED_AT_NAME is the name of the timestamp feature
    # We must include GENERATED_OBSERVED_AT_NAME in the __init__ signature, even if there is a timestamp
    # feature defined and named, because we cannot parse the class annotations until after the module is fully
    # loaded (otherwise we'll get circular errors when trying to resolve forward reference annotations)
    # So, we ALWAYS include the GENERATED_OBSERVED_AT_NAME as part of the signature, and then error if
    # that is not the name of the timestamp feature
    error_msg = f"{self_name}.__class__.__name__ + \".__init__() got unexpected value for argument '{GENERATED_OBSERVED_AT_NAME}'\""
    has_explicit_ts_feature = f"{self_name}.__chalk_ts__.attribute_name != '{GENERATED_OBSERVED_AT_NAME}'"
    specified_val_for_generated_observed_at = f"{GENERATED_OBSERVED_AT_NAME} is not MISSING"
    # Raising a TypeError to be consistent with an unexpected argument message
    body_lines.append(
        f"if {specified_val_for_generated_observed_at} and {has_explicit_ts_feature}: raise TypeError({error_msg})"
    )
    body_lines.append(field_assign(GENERATED_OBSERVED_AT_NAME, GENERATED_OBSERVED_AT_NAME, self_name))

    return create_fn(
        name="__init__",
        args=[self_name] + _init_params,
        body=body_lines,
        _locals=_locals,
        _globals=_globals,
        return_type=None,
    )


def _parse_tags(ts: str) -> List[str]:
    ts = re.sub(",", " ", ts)
    ts = re.sub(" +", " ", ts.strip())
    return [xx.strip() for xx in ts.split(" ")]


def _get_field(
    cls: Type,
    annotation_name: str,
    comments: Mapping[str, str],
    class_owner: Optional[str],
    class_tags: Optional[Tuple[str, ...]],
    class_etl_offline_to_online: Optional[bool],
    class_max_staleness: Optional[Duration],
    namespace: str,
) -> Feature:
    # Return a Field object for this field name and type.  ClassVars and
    # InitVars are also returned, but marked as such (see f._field_type).
    # default_kw_only is the value of kw_only to use if there isn't a field()
    # that defines it.

    # If the default value isn't derived from Field, then it's only a
    # normal default value.  Convert it to a Field().
    default = getattr(cls, annotation_name, ...)

    if isinstance(default, Feature):
        # The feature was set like x: int = Feature(...)
        f = default
        if f.version is not None:
            f.version.base_name = f._name or annotation_name
            f.name = f.version.name_for_version(f.version.default)
    elif isinstance(default, Windowed):
        # The feature was set like x: Windowed[int] = windowed()
        # Convert it to a Feature
        f = default._to_feature(bucket=None)
    else:
        # The feature was not set explicitly
        if isinstance(default, types.MemberDescriptorType):
            # This is a field in __slots__, so it has no default value.
            default = ...
        f = Feature(name=annotation_name, namespace=namespace, default=default)

    # Only at this point do we know the name and the type.  Set them.
    f.namespace = namespace
    f.typ = ParsedAnnotation(cls, annotation_name)

    f.features_cls = cls
    f.attribute_name = annotation_name
    _process_field(f, comments, class_owner, class_tags, class_etl_offline_to_online, class_max_staleness)
    return f


def _process_field(
    f: Feature,
    comments: Mapping[str, str],
    class_owner: Optional[str],
    class_tags: Optional[Tuple[str, ...]],
    class_etl_offline_to_online: Optional[bool],
    class_max_staleness: Optional[Duration],
) -> Feature:
    comment_for_feature = comments.get(f.attribute_name)
    comment_based_description = None
    comment_based_owner = None
    comment_based_tags = None

    if comment_for_feature is not None:
        comment_lines = []
        for line in comment_for_feature.splitlines():
            stripped_line = line.strip()
            if stripped_line.startswith(":owner:"):
                comment_based_owner = removeprefix(stripped_line, ":owner:").strip()
            elif stripped_line.startswith(":tags:"):
                parsed = _parse_tags(removeprefix(stripped_line, ":tags:"))
                if len(parsed) > 0:
                    if comment_based_tags is None:
                        comment_based_tags = parsed
                    else:
                        comment_based_tags.extend(parsed)
            else:
                comment_lines.append(line)

        comment_based_description = "\n".join(comment_lines)

    if f.description is None and comment_based_description is not None:
        f.description = comment_based_description

    if comment_based_tags is not None:
        if f.tags is None:
            f.tags = comment_based_tags
        else:
            f.tags.extend(comment_based_tags)

    if class_tags is not None:
        if f.tags is None:
            f.tags = list(class_tags)
        else:
            f.tags.extend(class_tags)

    if f.owner is not None and comment_based_owner is not None:
        raise ValueError(
            (
                f"Owner for {f.namespace}.{f.name} specified both on the feature and in the comment. "
                f"Please use only one of these two."
            )
        )
    elif f.owner is None:
        f.owner = comment_based_owner or class_owner

    if f.max_staleness is Ellipsis:
        f.max_staleness = class_max_staleness if class_max_staleness is not Ellipsis else None

    if f.etl_offline_to_online is None:
        f.etl_offline_to_online = False if class_etl_offline_to_online is None else class_etl_offline_to_online
    return f


def _recursive_repr(user_function: Callable[[T], str]) -> Callable[[T], str]:
    # Decorator to make a repr function return "..." for a recursive
    # call.
    repr_running = set()

    @functools.wraps(user_function)
    def wrapper(self: T):
        key = id(self), threading.get_ident()
        if key in repr_running:
            return "..."
        repr_running.add(key)
        try:
            result = user_function(self)
        finally:
            repr_running.discard(key)
        return result

    return wrapper


def _repr_fn(_globals: Dict[str, Any]):
    tuples = "((f.attribute_name, getattr(self, f.attribute_name, MISSING)) for f in self.features)"
    fn = create_fn(
        name="__repr__",
        args=["self"],
        body=[
            'return f"{self.__class__.__qualname__}(" + '
            + f"', '.join(f'{{x[0]}}={{x[1]}}' for x in {tuples} if x[1] != MISSING)"
            + '+ ")"'
        ],
        _globals=_globals,
        _locals={"MISSING": MISSING},
    )
    return _recursive_repr(fn)


def _eq_fn(_globals: Dict[str, Any]):
    cmp_str = "all(getattr(self, f.attribute_name, MISSING) == getattr(other, f.attribute_name, MISSING) for f in self.features)"
    return create_fn(
        name="__eq__",
        args=["self", "other"],
        body=[
            "if not isinstance(other, type(self)):",
            "    return NotImplemented",
            f"return {cmp_str}",
        ],
        _globals=_globals,
        _locals={
            "MISSING": MISSING,
        },
    )


def _len_fn(_globals: Dict[str, Any]):
    return create_fn(
        name="__len__",
        args=["self"],
        body=[
            "count = 0",
            f"for f in self.features:",
            "    if not f.no_display and hasattr(self, f.attribute_name):",
            "        count += 1",
            "return count",
        ],
        _globals=_globals,
        _locals={},
    )


def _iter_fn(_globals: Mapping[str, Any]):
    return create_fn(
        "__iter__",
        args=["self"],
        body=[
            f"for __chalk_f__ in self.features:",
            f"    if hasattr(self, __chalk_f__.attribute_name) and type(__chalk_f__).__name__ == 'Feature' and not __chalk_f__.is_has_one and not __chalk_f__.is_has_many and not __chalk_f__.no_display:",
            f"        yield __chalk_f__.fqn, getattr(self, __chalk_f__.attribute_name)",
        ],
    )


def _parse_annotation_comments(cls: Type) -> Mapping[str, str]:
    source = textwrap.dedent(inspect.getsource(cls))

    source_lines = source.splitlines()
    tree = ast.parse(source)
    if len(tree.body) != 1:
        return {}

    comments_for_annotations: Dict[str, str] = {}
    class_def = tree.body[0]
    if isinstance(class_def, ast.ClassDef):
        for stmt in class_def.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                line = stmt.lineno - 2
                comments: List[str] = []
                while line >= 0 and source_lines[line].strip().startswith("#"):
                    comment = source_lines[line].strip().strip("#").strip()
                    comments.insert(0, comment)
                    line -= 1

                if len(comments) > 0:
                    comments_for_annotations[stmt.target.id] = textwrap.dedent("\n".join(comments))

    return comments_for_annotations


def _process_class(
    cls: Type[T],
    owner: Optional[str],
    tags: Tuple[str, ...],
    etl_offline_to_online: Optional[bool],
    max_staleness: Optional[Duration],
    namespace: str,
) -> Type[T]:
    raw_cls_annotations = cls.__dict__.get("__annotations__", {})

    cls_annotations: Dict[str, Any] = {}
    for name, annotation in raw_cls_annotations.items():
        if isinstance(annotation, Windowed):
            # NOTE: For Windowed resolvers, both the Annotation and the value are instances of Windowed,
            # unlike normal features whose annotation is the underlying type, and the value is an instance
            # of FeatureWrapper. So both `annotation` and `wind` should be instances of Windowed
            # In the future, we should use a subclass of Windowed, rather than an instance, for the type annotation,
            # similar to what we do for Features
            wind = getattr(cls, name, None)
            if wind is None or not isinstance(wind, Windowed):
                assert annotation._kind is not None
                raise TypeError(
                    (
                        f"Windowed feature '{namespace}.{name}' is missing windows. "
                        f"To create a windowed feature, use "
                        f"'{name}: Windowed[{annotation._kind.__name__}] = windowed('10m', '30m')."
                    )
                )
            wind.kind = annotation.kind
            wind._name = name
            annotation._buckets = wind._buckets
            for bucket in wind._buckets:
                # Make pseudofeatures for each bucket of the window
                feat = wind._to_feature(bucket=bucket)
                setattr(cls, feat.name, feat)
                # For the psuedofeatures, which track an individual bucket, the correct annotation is the
                # underlying annotation, not Windowed[underlying], since it's only one value
                cls_annotations[feat.name] = wind.kind

        cls_annotations[name] = annotation

    if cls.__module__ in sys.modules:
        _globals = sys.modules[cls.__module__].__dict__
    else:
        _globals = {}

    # Find feature times that weren't annotated.
    for (name, member) in inspect.getmembers(cls):
        if name not in cls_annotations and isinstance(member, Windowed):
            raise TypeError(f"Windowed feature '{namespace}.{name}' is missing an annotation, like 'Windowed[str]'")
        if name not in cls_annotations and isinstance(member, Feature):
            # All feature types need annotations, except for datetimes, which we can automatically infer
            if member.typ is not None and member.typ.is_parsed:
                cls_annotations[name] = member.typ.annotation
            else:
                raise TypeError(f"Feature '{namespace}.{name}' is missing an annotation")

    cls.__annotations__ = cls_annotations

    # If we pass this function something that isn't a class, it could raise
    try:
        comments = _parse_annotation_comments(cls)
    except:
        comments = {}

    cls_fields: List[Feature] = []

    def __chalk_primary__(cls: Type[Features]):
        return _discover_feature(
            cls_fields,
            "primary",
            lambda f: f._primary is True,
            lambda f: f.typ.is_primary,
            lambda f: (
                f.name == "id" and not f.has_resolved_join and not f._is_feature_time and not f.typ.is_feature_time
            ),
        )

    set_new_attribute(cls, "__chalk_primary__", value=classproperty(__chalk_primary__, cached=True))

    def __chalk_ts__(cls: Type[Features]) -> Feature:
        # Not using `f.is_feature_time` as that would create an infinite recursion, since
        # `.is_feature_time` accesses `__chalk_ts__`
        ts_feature: Optional[Feature] = _discover_feature(
            cls_fields,
            "feature time",
            lambda f: f._is_feature_time is True,
            lambda f: f.typ.is_feature_time,
            lambda f: f.name == "ts" and not f.has_resolved_join and not f._primary and not f.typ.is_primary,
        )
        if ts_feature is None:
            return unwrap_feature(getattr(cls, GENERATED_OBSERVED_AT_NAME))
        return ts_feature

    set_new_attribute(cls=cls, name="__chalk_ts__", value=classproperty(__chalk_ts__, cached=True))

    def __chalk_observed_at__(cls: Type[Features]) -> Feature:
        ts_feature: Optional[Feature] = _discover_feature(
            cls_fields,
            "feature time",
            # Not using `f.is_feature_time` as that would create an infinite recursion, since
            # `.is_feature_time` accesses `__chalk_ts__` which can access this function
            lambda f: f._is_feature_time is True,
            lambda f: f.typ.is_feature_time,
            lambda f: f.name == "ts" and not f.has_resolved_join and not f._primary and not f.typ.is_primary,
        )
        if ts_feature is not None:
            if ts_feature.attribute_name != GENERATED_OBSERVED_AT_NAME:
                raise AttributeError(f"Object {cls.__name__} has no attribute '{GENERATED_OBSERVED_AT_NAME}")
        # If the timestamp feature is still none, then synthesize one on first use
        ts_feature = feature_time()
        assert ts_feature is not None
        ts_feature.name = GENERATED_OBSERVED_AT_NAME
        ts_feature.attribute_name = GENERATED_OBSERVED_AT_NAME
        ts_feature.namespace = cls.__chalk_namespace__
        ts_feature.features_cls = cls
        ts_feature.is_autogenerated = True
        cls.__annotations__[GENERATED_OBSERVED_AT_NAME] = datetime
        _process_field(
            ts_feature,
            comments={},
            class_owner=cls.__chalk_owner__,
            class_tags=tuple(cls.__chalk_tags__),
            class_etl_offline_to_online=cls.__chalk_etl_offline_to_online__,
            class_max_staleness=cls.__chalk_max_staleness__,
        )

        return FeatureWrapper(ts_feature)

    set_new_attribute(
        cls=cls,
        name=GENERATED_OBSERVED_AT_NAME,
        value=classproperty(__chalk_observed_at__, cached=True, bind_to_instances=False),
    )

    def __features__(cls: Features) -> List[Feature]:
        features = list(cls_fields)
        if cls.__chalk_ts__ not in features:
            features.append(cls.__chalk_ts__)
        return features

    set_new_attribute(cls=cls, name="features", value=classproperty(__features__, cached=True))
    set_new_attribute(cls=cls, name="__repr__", value=_repr_fn(_globals=_globals))
    set_new_attribute(cls=cls, name="__eq__", value=_eq_fn(_globals=_globals))
    set_new_attribute(cls=cls, name="__hash__", value=None)
    set_new_attribute(cls=cls, name="__iter__", value=_iter_fn(_globals=_globals))

    set_new_attribute(cls=cls, name="namespace", value=namespace)
    set_new_attribute(cls=cls, name="__chalk_namespace__", value=namespace)
    set_new_attribute(cls=cls, name="__chalk_owner__", value=owner)
    set_new_attribute(cls=cls, name="__chalk_tags__", value=list(tags))
    set_new_attribute(
        cls=cls, name="__chalk_max_staleness__", value=max_staleness if max_staleness is not Ellipsis else None
    )
    set_new_attribute(
        cls=cls,
        name="__chalk_etl_offline_to_online__",
        value=etl_offline_to_online if etl_offline_to_online is not Ellipsis else False,
    )
    set_new_attribute(cls=cls, name="__is_features__", value=True)
    set_new_attribute(cls=cls, name="__len__", value=_len_fn(_globals=_globals))
    set_new_attribute(cls=cls, name="__getattribute__", value=_getattribute_fn(_globals=_globals))
    # Moving this line lower causes all kinds of problems.
    cls = classproperty_support(cls)

    # Parse the fields after we have the correct `cls` set
    cls_fields.extend(
        _get_field(
            cls=cls,
            annotation_name=name,
            comments=comments,
            class_owner=owner,
            class_tags=tags,
            class_etl_offline_to_online=etl_offline_to_online,
            class_max_staleness=max_staleness,
            namespace=namespace,
        )
        for name in cls_annotations
    )

    alias_from_to: Dict[str, str] = {}

    # We're appending to this list
    for f in islice(cls_fields, len(cls_fields)):
        if f.version is None:
            continue
        alias_from_to[f.attribute_name] = f"{f.attribute_name}_v{f.version.default}"

        for i in range(1, f.version.maximum + 1):
            f_i = copy.copy(f)
            f_i.name = f.version.name_for_version(i)
            f_i.attribute_name = f"{f.attribute_name}_v{i}"
            f_i.version = _VersionInfo(
                version=i,
                maximum=f.version.maximum,
                default=f.version.default,
                reference=f.version.reference,
            )
            f.version.reference[i] = f_i
            cls_fields.append(f_i)

            # The default feature already exists.
            f_i.no_display = i == f.version.default

            if f_i.attribute_name in cls_annotations:
                assert f_i.features_cls is not None
                raise ValueError(
                    f"The class '{f_i.features_cls.__name__}' "
                    f"has an existing annotation '{f_i.attribute_name}' "
                    "that collides with a versioned feature. Please remove the existing "
                    "annotation, or lower the version."
                )

    set_new_attribute(
        cls=cls,
        name="__setattr__",
        value=_setattr_fn(
            bidirectional_alias=dict({v: k for k, v in alias_from_to.items()}, **alias_from_to),
            _globals=_globals,
        ),
    )
    set_new_attribute(
        cls=cls,
        name="__init__",
        value=_init_fn(
            feature_names_and_annotations=[(x.attribute_name, x.typ.annotation) for x in cls_fields],
            alias_from_to=alias_from_to,
            _globals=_globals,
        ),
    )

    for f in cls_fields:
        assert f.attribute_name is not None
        # Wrap all class features with FeatureWrapper
        setattr(cls, f.attribute_name, FeatureWrapper(f))

    return cls
