from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any, Generic, List, Literal, Mapping, Optional, Set, Type, TypeVar, Union, cast

from chalk._validation.feature_validation import FeatureValidation
from chalk.features._encoding.primitive import TPrimitive
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import Duration, parse_chalk_duration, timedelta_to_duration

T = TypeVar("T")
TPrim = TypeVar("TPrim", bound=TPrimitive)
TRich = TypeVar("TRich")

if TYPE_CHECKING:
    import polars as pl

    from chalk.features._encoding.converter import TDecoder, TEncoder


class WindowedInstance(Generic[T]):
    def __init__(self, values: Mapping[str, T]):
        self.values = values

    def __call__(self, period: str):
        return self.values[period]


class WindowedMeta(type, Generic[T]):
    def __getitem__(cls, underlying: Type[T]) -> "Windowed[Type[T]]":
        return Windowed(
            kind=underlying,
            buckets=[],
            mode="tumbling",
            description=None,
            owner=None,
            tags=None,
            name=None,
            default=None,
            max_staleness=None,
            version=None,
            etl_offline_to_online=None,
            encoder=None,
            decoder=None,
            min=None,
            max=None,
            min_length=None,
            max_length=None,
            contains=None,
            dtype=None,
        )  # noqa


JsonValue = Any


def get_duration_secs(duration: Union[str, int, timedelta]) -> int:
    if isinstance(duration, str):
        duration = parse_chalk_duration(duration)
    if isinstance(duration, timedelta):
        duration_secs_float = duration.total_seconds()
        duration_secs_int = int(duration_secs_float)
        if duration_secs_float != duration_secs_int:
            raise ValueError("Windows that are fractions of seconds are not yet supported")
        duration = duration_secs_int
    return duration


def get_name_with_duration(name_or_fqn: str, duration: Union[str, int, timedelta]) -> str:
    duration_secs = get_duration_secs(duration)
    return f"{name_or_fqn}__{duration_secs}__"


class Windowed(Generic[TPrim, TRich], metaclass=WindowedMeta):
    """Declare a windowed feature.

    Examples
    --------
    >>> @features
    ... class User:
    ...     failed_logins: Windowed[int] = windowed("10m", "24h")
    """

    _mode: Literal["tumbling", "continuous"]

    @property
    def buckets_seconds(self) -> Set[int]:
        return set(int(parse_chalk_duration(bucket).total_seconds()) for bucket in self._buckets)

    @property
    def kind(self) -> Type[TRich]:
        if self._kind is None:
            raise RuntimeError("Window type has not yet been parsed")
        return self._kind

    @kind.setter
    def kind(self, kind: Type[TRich]) -> None:
        assert self._kind is None, "Window type cannot be set twice"
        self._kind = kind

    def _to_feature(self, bucket: Optional[Union[int, str]]):
        from chalk.features import Feature

        assert self._name is not None

        if bucket is None:
            name = self._name
        else:
            if get_duration_secs(bucket) not in self.buckets_seconds:
                raise ValueError(f"Bucket {bucket} is not in the list of specified buckets")
            name = get_name_with_duration(self._name, bucket)

        return Feature(
            name=name,
            version=self._version,
            owner=self._owner,
            tags=None if self._tags is None else list(ensure_tuple(self._tags)),
            description=self._description,
            primary=False,
            default=self._default,
            max_staleness=(
                timedelta_to_duration(self._max_staleness)
                if isinstance(self._max_staleness, timedelta)
                else self._max_staleness
            ),
            etl_offline_to_online=self._etl_offline_to_online,
            encoder=self._encoder,
            decoder=self._decoder,
            pyarrow_dtype=self._dtype,
            validations=FeatureValidation(
                min=self._min,
                max=self._max,
                min_length=self._min_length,
                max_length=self._max_length,
                contains=self._contains,
            ),
            # Only the root feature should have all the durations
            # The pseudofeatures, which are bound to a duration, should not have the durations
            # of the other buckets
            window_durations=tuple(self.buckets_seconds) if bucket is None else tuple(),
            window_duration=None if bucket is None else get_duration_secs(bucket),
            window_mode=self._mode,
        )

    def __init__(
        self,
        buckets: List[str],
        mode: Literal["tumbling", "continuous"],
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Any],
        name: Optional[str],
        default: Union[TRich, ellipsis],
        max_staleness: Union[Duration, None, ellipsis],
        version: Optional[int],
        etl_offline_to_online: Optional[bool],
        encoder: Optional[TEncoder[TPrim, TRich]],
        decoder: Optional[TDecoder[TPrim, TRich]],
        min: Optional[TRich],
        max: Optional[TRich],
        min_length: Optional[int],
        max_length: Optional[int],
        contains: Optional[TRich],
        dtype: Optional[Union[Type[pl.DataType], pl.DataType]],
        kind: Optional[Type[TRich]],
    ):
        self._kind = kind
        self._name: Optional[str] = None
        self._buckets = buckets
        self._mode = mode
        self._description = description
        self._owner = owner
        self._tags = tags
        self._name = name
        self._default = default
        self._max_staleness = max_staleness
        self._description = description
        self._version = version
        self._etl_offline_to_online = etl_offline_to_online
        self._encoder = encoder
        self._decoder = decoder
        self._min = min
        self._max = max
        self._min_length = min_length
        self._max_length = max_length
        self._contains = contains
        self._dtype = dtype


class SelectedWindow:
    def __init__(self, kind: Windowed, selected: str):
        self.windowed = kind
        self.selected = selected


def windowed(
    *buckets: str,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Any] = None,
    name: Optional[str] = None,
    default: Union[T, None, ellipsis] = ...,
    max_staleness: Union[Duration, None, ellipsis] = ...,
    version: Optional[int] = None,
    etl_offline_to_online: Optional[bool] = None,
    encoder: Optional[TEncoder[TPrim, TRich]] = None,
    decoder: Optional[TDecoder[TPrim, TRich]] = None,
    min: Optional[T] = None,
    max: Optional[T] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    contains: Optional[T] = None,
    dtype: Optional[Union[Type[pl.DataType], pl.DataType]] = None,
    # Deprecated
    mode: Literal["tumbling", "continuous"] = "tumbling",
) -> Windowed[TPrim, TRich]:
    """Create a windowed feature.

    See more at https://docs.chalk.ai/docs/aggregations#windowed-features

    Parameters
    ----------
    buckets
        The size of the buckets for the window function.
    default
        The default value of the feature if it otherwise can't be computed.
    owner
        You may also specify which person or group is responsible for a feature.
        The owner tag will be available in Chalk's web portal.
        Alerts that do not otherwise have an owner will be assigned
        to the owner of the monitored feature.
    tags
        Add metadata to a feature for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
    max_staleness
        When a feature is expensive or slow to compute, you may wish to cache its value.
        Chalk uses the terminology "maximum staleness" to describe how recently a feature
        value needs to have been computed to be returned without re-running a resolver.

        Read more at https://docs.chalk.ai/docs/feature-caching
    version
        Feature versions allow you to manage a feature as its
        definition changes over time.

        The `version` keyword argument allows you to specify the
        maximum number of versions available for this feature.

        See more at https://docs.chalk.ai/docs/feature-versions
    etl_offline_to_online
        When `True`, Chalk copies this feature into the online environment
        when it is computed in offline resolvers.

        Read more at https://docs.chalk.ai/docs/reverse-etl
    min
        If specified, when this feature is computed, Chalk will check that `x >= min`.
    max
        If specified, when this feature is computed, Chalk will check that `x <= max`.
    min_length
        If specified, when this feature is computed, Chalk will check that `len(x) >= min_length`.
    max_length
        If specified, when this feature is computed, Chalk will check that `len(x) <= max_length`.
    contains

    Other Parameters
    ----------------
    name
        The name for the feature. By default, the name of a feature is
        the name of the attribute on the class, prefixed with
        the camel-cased name of the class. Note that if you provide an
        explicit name, the namespace, determined by the feature class,
        will still be prepended. See `features` for more details.
    description
        Descriptions are typically provided as comments preceding
        the feature definition. For example, you can document a
        `email_count` feature with information about the values
        as follows::
        >>> @features
        ... class User:
        ...     # Count of emails sent
        ...     email_count: Windowed[int] = windowed("10m", "30m")

        You can also specify the description directly with this parameter.
        >>> @features
        ... class User:
        ...     email_count: Windowed[int] = windowed(
        ...         "10m", "30m"
        ...         description="Count of emails sent",
        ...     )
    encoder
    decoder
    dtype
    mode

    Returns
    -------
    Windowed[TPrim, TRich]
        Metadata for the windowed feature, parameterized by
        `TPrim` (the primitive type of the feature) and
        `TRich` (the decoded type of the feature, if `decoder` is provided).
    """
    return Windowed(
        list(buckets),
        mode=mode,
        description=description,
        owner=owner,
        tags=tags,
        name=name,
        default=default,
        max_staleness=max_staleness,
        version=version,
        etl_offline_to_online=etl_offline_to_online,
        encoder=cast("TEncoder", encoder),
        decoder=decoder,
        min=min,
        max=max,
        min_length=min_length,
        max_length=max_length,
        contains=contains,
        dtype=dtype,
        kind=None,
    )
