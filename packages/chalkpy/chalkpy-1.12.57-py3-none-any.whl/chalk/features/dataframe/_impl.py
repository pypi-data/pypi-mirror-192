from __future__ import annotations

import base64
import collections.abc
import inspect
import json
import operator
import os
import pathlib
import typing
import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

import pyarrow as pa
from pydantic import BaseModel

from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features.dataframe._filters import filter_data_frame
from chalk.features.dataframe._validation import validate_df_schema, validate_nulls
from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper, ensure_feature
from chalk.features.filter import Filter
from chalk.utils.collections import ensure_tuple, get_unique_item
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

    from chalk.features.feature_set import Features
    from chalk.sql import ChalkQueryProtocol, FinalizedChalkQuery, StringChalkQueryProtocol

else:
    try:
        import pandas as pd
    except ImportError:
        pd = None


TDataFrame = TypeVar("TDataFrame", bound="DataFrame")


class DataFrameMeta(type):
    # Annotating __getitem__ return a union of DataFrame, query, or string to support resolvers that return sql queries
    def __getitem__(
        cls, item: Any
    ) -> Union[
        Type[DataFrame],
        Type[ChalkQueryProtocol],
        Type[StringChalkQueryProtocol],
        Type[FinalizedChalkQuery],
        Type[str],
    ]:
        from chalk.features.feature_set import Features

        # leaving untyped as we type the individual features as their object type
        # but item should really be Filter (expressions), Feature classes, or Feature instances
        cls = cast(Type[DataFrame], cls)

        item = ensure_tuple(item)

        # Disallow string annotations like DataFrame["User"].
        # Instead, the entire thing should be in quotes -- like "DataFrame[User]"
        for x in item:
            if isinstance(x, str):
                raise TypeError(
                    (
                        f'Annotation {cls.__name__}["{x}", ...] is unsupported. Instead, use a string for the entire annotation -- for example: '
                        f'"{cls.__name__}[{x}, ...]"'
                    )
                )

        # If doing multiple subscript, then keep the filters, but do not keep the individual columns
        # TODO: Validate that any new columns are a subset of the existing columns
        item = [*item, *cls.filters]

        new_filters: List[Filter] = []
        new_references_feature_set: Optional[Type[Features]] = None
        new_columns: List[Feature] = []
        pydantic_model = None

        for a in item:
            if isinstance(a, Filter):
                new_filters.append(a)
            elif isinstance(a, type) and issubclass(a, Features):
                if new_references_feature_set is not None:
                    raise ValueError(
                        f"Multiple referenced feature sets -- {new_references_feature_set} and {a} -- are not supported."
                    )
                new_references_feature_set = a
            elif isinstance(a, Feature):
                new_columns.append(a)
            elif isinstance(a, FeatureWrapper):
                new_columns.append(a._chalk_feature)
            elif isinstance(a, bool):
                # If we encounter a bool, that means we are evaluating the type annotation before
                # the ResolverAstParser had a chance to extract the source and rewrite the and/or/in operations
                # into expressions that return filters instead of booleans
                # This function will be called again for this annotation, so we can ignore it for now.
                pass
            elif inspect.isclass(a) and issubclass(a, BaseModel):
                pydantic_model = a
            else:
                raise TypeError(f"Invalid type for DataFrame[{a}]: {type(a)}")

        if len(new_columns) == 0 and new_references_feature_set is None:
            # This is possible if you have something like
            # Users.transactions[after('60d')]
            # In this case, keep all existing columns
            # But if you did
            # Users.transactions[Transaction.id, after('60d')]
            # Then keep only the id column
            new_columns = list(cls.__columns__)
            new_references_feature_set = cls.__references_feature_set__

        class SubclassedDataFrame(cls):
            filters = tuple(new_filters)
            __columns__ = tuple(new_columns)
            __references_feature_set__ = new_references_feature_set
            __pydantic_model__ = pydantic_model

            def __new__(cls: Type[TDataFrame], *args: Any, **kwargs: Any) -> TDataFrame:
                raise RuntimeError(
                    "A SubclassedDataFrame should never be instantiated. Instead, instantiate a DataFrame(...)."
                )

        return SubclassedDataFrame

    def __repr__(cls):
        cls = cast(Type[DataFrame], cls)
        elements = [str(x) for x in (*cls.filters, *cls.columns)]
        return f"DataFrame[{', '.join(elements)}]"

    @property
    def columns(cls) -> Tuple[Feature, ...]:
        # Computing the columns lazily as we need to implicitly parse the type annotation
        # to determine if a field is a has-many, and we don't want to do that on the
        # __getitem__ which could happen before forward references can be resolved
        # So, using a property on the metaclass, which acts like an attribute on the class, to
        # provide the dataframe columns
        from chalk.features.feature_field import Feature

        cls = cast(Type[DataFrame], cls)
        columns: Set[Feature] = set()
        for x in cls.__columns__:
            assert isinstance(x, Feature)
            # If a feature is directly specified, allow has-ones. But still do not allow has-many features
            assert not x.is_has_many, "Has-many features are not allowed to be specified within a DataFrame"
            columns.add(x)
        if cls.__references_feature_set__ is not None:
            # Only include the first-level feature types
            # Do not recurse has-ones and has-many as that could create an infinite loop
            for x in cls.__references_feature_set__.features:
                assert isinstance(x, Feature)
                if not x.is_has_many and not x.is_has_one:
                    columns.add(x)
        return tuple(columns)

    @property
    def references_feature_set(cls):
        from chalk.features.feature_set import FeatureSetBase

        cls = cast(Type[DataFrame], cls)
        if cls.__references_feature_set__ is not None:
            return cls.__references_feature_set__
        else:
            # Determine the unique @features cls that encompasses all columns
            root_ns = get_unique_item((x.root_namespace for x in cls.__columns__), "root ns")
        return FeatureSetBase.registry[root_ns]

    @property
    def namespace(cls) -> str:
        cls = cast(Type[DataFrame], cls)
        namespaces = [x.path[0].parent.namespace if len(x.path) > 0 else x.namespace for x in cls.columns]
        # Remove the pseudo-columns
        namespaces = [x for x in namespaces if not x.startswith("__chalk__")]
        return get_unique_item(namespaces, f"dataframe {cls.__name__} column namespaces")


class DataFrameImpl(metaclass=DataFrameMeta):
    filters: ClassVar[Tuple[Filter, ...]] = ()
    columns: Tuple[Feature, ...]  # set via a @property on the metaclass
    __columns__: ClassVar[Tuple[Feature, ...]] = ()
    references_feature_set: Optional[Type[Features]]  # set via a @property on the metaclass
    __references_feature_set__: ClassVar[Optional[Type[Features]]] = None
    __pydantic_model__: ClassVar[Optional[Type[BaseModel]]] = None

    def __init__(
        self,
        data: Union[
            Dict[Union[str, Feature, FeatureWrapper, Any], Sequence[Any]],
            Sequence[Union[Features, Any]],
            pl.DataFrame,
            pl.LazyFrame,
            pd.DataFrame,
            Any,  # Polars supports a bunch of other formats for initialization of a DataFrame
        ] = None,
        # Setting to default_or_allow for backwards compatibility
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        pandas_dataframe: Optional[pd.DataFrame] = None,  # For backwards compatibility
        # By default, data should match the dtype of the feature.
        # However, when doing comparisons, data will be converted to bools,
        # in which case the data types should no longer be converted.
        # This is an undocumented parameters so it does not appear in the docstring
        convert_dtypes: bool = True,
        pydantic_model: Optional[Type[BaseModel]] = None,
    ):
        """Construct a Chalk `DataFrame`.

        Parameters
        ----------
        data
            The data. Can be an existing `pandas.DataFrame`,
            `polars.DataFrame` or `polars.LazyFrame`,
            a sequence of feature instances, or a `dict` mapping
            a feature to a sequence of values.
        missing_value_strategy
            The strategy to use to handle missing values.

            A feature value is "missing" if it is an ellipsis (`...`),
            or it is `None` and the feature is not annotated as `Optional[...]`.

            The available strategies are:
                `'error'`: Raise a `TypeError` if any missing values are found.
                    Do not attempt to replace missing values with the default
                    value for the feature.
                `'default_or_error'`: If the feature has a default value, then
                    replace missing values with the default value for the feature.
                    Otherwise, raise a `TypeError`.
                `'default_or_allow'`:  If the feature has a default value, then
                    replace missing values with the default value for the feature.
                    Otherwise, leave it as `None`. This is the default strategy.
                `'allow'`: Allow missing values to be stored in the `DataFrame`.
                    This option may result non-nullable features being assigned
                    `None` values.
        """
        from chalk.features.feature_set import Features, FeatureSetBase

        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        self._pydantic_model = pydantic_model
        self._convert_dtypes = convert_dtypes

        # Typing the keys of ``data`` as Any, as {FeatureCls.item: x} would be typed as the underlying annotation
        # of the features cls
        if pandas_dataframe is not None:
            warnings.warn(
                DeprecationWarning("ChalkDataFrameImpl(pandas_dataframe=...) has been renamed to DataFrame(data=...)")
            )
            data = pandas_dataframe
        if pd is not None and isinstance(data, pd.DataFrame):
            # Convert the columns to root fqn strings
            # str(Feature) and str(FeatureWrapper) return the root fqns
            data = data.rename(columns={k: str(k) for k in data.columns})
            assert isinstance(data, pd.DataFrame)
            data.columns = data.columns.astype("string")
            data = pl.from_pandas(data)
        if not isinstance(data, (pl.LazyFrame, pl.DataFrame)):
            if isinstance(data, (collections.abc.Sequence)) and not isinstance(data, str):
                # If it is a sequence, it could be a sequence of feature classes instances
                # If so, set the columns by inspecting the feature classes
                # If columns are none, then inspect the data to determine if they are feature classes
                # Otherwise, if the columns are specified, do not introspect the list construction
                features_typ = None
                new_data: dict[str, list[Any]] = {}
                for row in data:
                    if not isinstance(row, Features):
                        raise ValueError("If specifying data as a sequence, it must be a sequence of Features")
                    if features_typ is None:
                        features_typ = type(row)
                        for x in row.features:
                            assert isinstance(x, Feature)
                            assert x.attribute_name is not None
                            try:
                                feature_val = getattr(row, x.attribute_name)
                            except AttributeError:
                                continue
                            new_data[x.root_fqn] = []

                    if features_typ != type(row):
                        raise ValueError("Cannot mix different feature classes in a DataFrame")
                    for x in row.features:
                        assert isinstance(x, Feature)
                        assert x.attribute_name is not None
                        try:
                            feature_val = getattr(row, x.attribute_name)
                        except AttributeError:
                            if x.root_fqn in new_data:
                                raise ValueError(f"Feature {x.root_fqn} is not defined in all feature sets.")
                            continue
                        if x.is_has_many:
                            raise ValueError("DataFrames within DataFrames are not supported")
                        if x.root_fqn not in new_data:
                            raise ValueError(f"Feature {x.root_fqn} is not defined in all feature sets.")
                        new_data[x.root_fqn].append(feature_val)
                data = new_data
            if isinstance(data, dict):
                # Convert the columns to root fqn strings
                new_data_dict: Dict[str, Union[Sequence[Any], pl.Series]] = {}
                for k, v in data.items():
                    feature = Feature.from_root_fqn(str(k))

                    if feature.is_has_one or feature.is_has_many:
                        name = "has-one" if feature.is_has_one else "has-many"
                        warnings.warn(
                            DeprecationWarning(
                                (
                                    f"Feature '{feature}' is a {name} feature. Its values will not be validated, "
                                    f"nor can this column be used for filtering. Support for passing {name} features "
                                    "into a Chalk DataFrame will be removed. Instead, specify each feature of the "
                                    "nested feature class as an individual column."
                                )
                            )
                        )
                        series = pl.Series(v, dtype=pl.Object)
                    else:
                        if convert_dtypes:
                            try:
                                pa_array = feature.converter.from_rich_to_pyarrow(
                                    v,
                                    missing_value_strategy=missing_value_strategy,
                                )
                            except (TypeError, ValueError) as e:
                                raise TypeError(
                                    (
                                        f"The values for feature `{k}` could not be loaded into a DataFrame column "
                                        f"of type `{feature.converter.pyarrow_dtype}`"
                                    )
                                ) from e
                            series = pl.from_arrow(pa_array)
                            assert isinstance(series, pl.Series)
                        else:
                            series = v
                    new_data_dict[str(k)] = series

                data = new_data_dict
            data = pl.DataFrame(data)
        if isinstance(data, (pl.LazyFrame, pl.DataFrame)):
            underlying = data
        else:
            raise ValueError(f"Unable to convert data of type {type(data).__name__} into a DataFrame")
        # Rename / validate that all column names are root fqns
        if self._pydantic_model is None:
            self.columns = tuple(Feature.from_root_fqn(str(c)) for c in underlying.columns)
            underlying = underlying.rename(
                {original_c: new_c.root_fqn for (original_c, new_c) in zip(underlying.columns, self.columns)}
            )
        else:
            self.columns = ()

        # Convert columns to the correct dtype to match the fqn
        if self._pydantic_model is None and convert_dtypes:
            underlying = validate_df_schema(underlying)
            underlying = validate_nulls(underlying, missing_value_strategy=missing_value_strategy)

        if isinstance(underlying, pl.DataFrame):
            underlying = underlying.lazy()
        self._underlying = underlying

        # Remove the pseudo-features when determining the namespace
        namespaces = (x.path[0].parent.namespace if len(x.path) > 0 else x.namespace for x in self.columns)
        namespaces_set = set(x for x in namespaces if not x.startswith("__chalk__"))
        if len(namespaces_set) == 1:
            self.namespace = get_unique_item(namespaces_set, f"dataframe column namespaces")
            self.references_feature_set = FeatureSetBase.registry[self.namespace]
        else:
            # Allow empty dataframes or dataframes with multiple namespaces
            self.namespace = None
            self.references_feature_set = None

    ##############
    # Classmethods
    ##############

    @classmethod
    def from_dict(
        cls: Type[TDataFrame],
        data: Dict[Union[str, Feature, FeatureWrapper, Any], Sequence[Any]],
    ) -> TDataFrame:
        warnings.warn(DeprecationWarning("DataFrame.from_dict(...) is deprecated. Instead, use DataFrame(...)"))
        df = cls(data)
        return df

    @overload
    @classmethod
    def from_list(
        cls: Type[TDataFrame],
        data: Sequence[Features],
        /,
    ) -> TDataFrame:
        ...

    @overload
    @classmethod
    def from_list(cls: Type[TDataFrame], *data: Features) -> TDataFrame:
        ...

    @classmethod
    def from_list(cls: Type[TDataFrame], *data: Union[Features, Sequence[Features]]) -> TDataFrame:
        warnings.warn(DeprecationWarning("DataFrame.from_list(...) is deprecated. Instead, use DataFrame(...)"))
        if len(data) == 1 and isinstance(data[0], collections.abc.Sequence):
            # Passed a list as the first argument
            features_seq = data[0]
        else:
            data = cast("Tuple[Features]", data)
            features_seq = data
        df = cls(features_seq)
        return df

    @classmethod
    def _get_storage_options(cls) -> typing.Optional[Dict[str, Any]]:
        if os.getenv("GCP_INTEGRATION_CREDENTIALS_B64") is not None:
            try:
                from google.oauth2 import service_account
            except ImportError:
                raise missing_dependency_exception("google-auth")
            token = service_account.Credentials.from_service_account_info(
                json.loads(base64.b64decode(os.getenv("GCP_INTEGRATION_CREDENTIALS_B64"))),
                scopes=[
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/userinfo.email",
                ],
            )
            return {"token": token}
        else:
            return None

    @classmethod
    def read_parquet(
        cls: Type[TDataFrame],
        path: Union[str, pathlib.Path],
        columns: Optional[
            Union[
                Dict[str, Union[str, Feature, Any]],
                Dict[int, Union[str, Feature, Any]],
            ]
        ] = None,
    ) -> TDataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        if columns is None:
            cols_to_select, _, new_columns = None, None, None
        else:
            cols_to_select, _, new_columns = cls._parse_columns(columns)

        data = pl.read_parquet(
            source=path,
            columns=cols_to_select,
            storage_options=DataFrame._get_storage_options(),
        )
        if new_columns is not None:
            data = data.rename({c: new_columns[i] for i, c in enumerate(data.columns)})
        return cls(data)

    @classmethod
    def _parse_columns(
        cls,
        col_mapping: Union[
            Dict[str, Union[str, Feature, FeatureWrapper, Any]],
            Dict[int, Union[str, Feature, FeatureWrapper, Any]],
        ],
    ) -> Tuple[Union[List[str], List[int]], List[Type[pl.DataType]], List[str]]:
        if not isinstance(col_mapping, dict):
            raise ValueError(f"Invalid column mapping. Received '{type(col_mapping).__name__}'; expected dict")
        columns = []
        dtypes = []
        new_cols: List[str] = []
        for k, v in col_mapping.items():
            columns.append(k)
            new_cols.append(str(v))
            dtypes.append(ensure_feature(v).converter.polars_dtype)
        return columns, dtypes, new_cols

    @classmethod
    def read_csv(
        cls: Type[TDataFrame],
        path: Union[str, pathlib.Path],
        has_header: bool = True,
        columns: Optional[
            Union[
                Dict[str, Union[str, Feature, Any]],
                Dict[int, Union[str, Feature, Any]],
            ]
        ] = None,
    ) -> TDataFrame:
        """Read a .csv file as a `DataFrame`.

        Parameters
        ----------
        path
            The path to the .csv file. This may be a S3 or GCS
            storage url.
        has_header
            Whether the .csv file has a header row as the first row.
        columns
            A mapping of index to feature name.

        Returns
        -------
        TDataFrame
            A `DataFrame` with the contents of the file loaded as features.

        Examples
        --------
        >>> values = DataFrame.read_csv(
        ...     "s3://...",
        ...     columns={0: MyFeatures.id, 1: MyFeatures.name},
        ...     has_header=False,
        ... )
        """
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        if columns is None:
            cols_to_select, dtypes, new_columns = None, None, None
        else:
            cols_to_select, dtypes, new_columns = cls._parse_columns(columns)

        data = pl.read_csv(
            file=path,
            has_header=has_header,
            columns=cols_to_select,
            dtypes=dtypes,
            new_columns=new_columns,
            storage_options=DataFrame._get_storage_options(),
        )
        return cls(data)

    #############
    # Aggregation
    #############

    def max(self):
        return DataFrame(self._underlying.max(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def mean(self):
        return DataFrame(self._underlying.mean(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def median(self):
        return DataFrame(self._underlying.median(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def min(self):
        return DataFrame(self._underlying.min(), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def std(self, ddof: int = 1):
        return DataFrame(self._underlying.std(ddof), convert_dtypes=False, pydantic_model=self._pydantic_model)

    def sum(self):
        # Treat missing sums as zero
        return DataFrame(
            self._underlying.sum().fill_null(0),
            convert_dtypes=False,
            pydantic_model=self._pydantic_model,
        )

    def var(self, ddof: int = 1):
        return DataFrame(self._underlying.var(ddof), convert_dtypes=False, pydantic_model=self._pydantic_model)

    ####################
    # Summary Operations
    ####################

    # These ops require us to materialize the dataframe.

    def _materialize(self) -> pl.DataFrame:
        materialized = self._underlying.collect()
        self._underlying = materialized.lazy()
        return materialized

    def any(self):
        """Returns whether any of the values in the dataframe are truthy.
        Requires the dataframe to only contain boolean values."""
        import polars as pl

        if len(self) == 0:
            return False
        if not all(isinstance(x, type) and issubclass(x, pl.Boolean) for x in self._underlying.dtypes):
            raise TypeError("DataFrame.any() is not defined on a dataframe that contains non-boolean columns.")
        materialized = self._materialize()
        return any(col.any() for col in materialized.get_columns())

    def all(self):
        """Returns whether all of the values in the dataframe are truthy. Requires the dataframe to only contain boolean values."""
        import polars as pl

        if len(self) == 0:
            return True
        if not all(isinstance(x, type) and issubclass(x, pl.Boolean) for x in self._underlying.dtypes):
            raise TypeError("DataFrame.any() is not defined on a dataframe that contains non-boolean columns.")
        materialized = self._materialize()
        return all(col.all() for col in materialized.get_columns())

    def __len__(self):
        materialized = self._materialize()
        return len(materialized)

    @property
    def shape(self):
        materialized = self._materialize()
        return materialized.shape

    def item(self):
        """Get the only item from the dataframe."""
        materialized = self._materialize()
        if materialized.shape == (1, 1):
            return materialized.rows()[0][0]
        raise ValueError(
            "The dataframe contains multiple items. DataFrame.item() can only be used if the dataframe has a single element."
        )

    def __bool__(self):
        if self.shape == (1, 1):
            # It's a dataframe of 1 item. self.any() and self.all() would return the same thing
            return self.all()
        raise ValueError("__bool__ is ambiguous on a DataFrame. Instead, use DataFrame.any() or DataFrame.all().")

    def __str__(self):
        materialized = self._materialize()
        return str(materialized)

    def __repr__(self):
        materialized = self._materialize()
        return repr(materialized)

    def __float__(self):
        return float(self.item())

    def __int__(self):
        return int(self.item())

    ############################
    # Arithmetic and Comparisons
    ############################

    # These ops require us to materialize the dataframe.

    def _perform_op(
        self,
        op: Union[str, Callable[[Any, Any], Any]],
        other: Union[DataFrame, pl.DataFrame, pd.DataFrame, Any],
        convert_dtypes: bool,
    ):
        import polars as pl

        materialized = self._materialize()
        if isinstance(other, DataFrame):
            other = other.to_polars()
        if isinstance(other, pl.LazyFrame):
            other = other.collect()
        if pd is not None and isinstance(other, pd.DataFrame):
            other = pl.from_pandas(other)
        if op in ("eq", "ne", "lt", "le", "ge", "gt"):
            if isinstance(other, pl.DataFrame):
                return self._perform_comp_df(op, other, convert_dtypes=convert_dtypes)
            else:
                return DataFrame(
                    getattr(operator, op)(materialized, other),
                    convert_dtypes=convert_dtypes,
                    pydantic_model=self._pydantic_model,
                )
        assert callable(op)
        return DataFrame(
            op(materialized, other),
            convert_dtypes=convert_dtypes,
            pydantic_model=self._pydantic_model,
        )

    def _perform_comp_df(
        self,
        op: str,
        other: pl.DataFrame,
        convert_dtypes: bool,
    ):
        # There's a bug in the default polars implementation for comparisons -- see
        # https://github.com/pola-rs/polars/issues/5870
        import polars as pl

        materialized = self._materialize()
        if set(materialized.columns) != set(other.columns):
            raise ValueError(f"DataFrame columns do not match. {materialized.columns} != {other.columns}")
        # Put the columns in the same order
        other = other.select(materialized.columns)
        if materialized.shape != other.shape:
            raise ValueError("DataFrame dimensions do not match")

        suffix = "__POLARS_CMP_OTHER"
        other_renamed = other.select(pl.all().suffix(suffix))
        combined = pl.concat([materialized, other_renamed], how="horizontal")

        if op == "eq":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(True))
                    .otherwise(pl.col(n) == pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        elif op == "ne":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(False))
                    .otherwise(pl.col(n) != pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        elif op == "gt":
            expr = [pl.col(n) > pl.col(f"{n}{suffix}") for n in materialized.columns]
        elif op == "lt":
            expr = [pl.col(n) < pl.col(f"{n}{suffix}") for n in materialized.columns]
        elif op == "ge":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(True))
                    .otherwise(pl.col(n) >= pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        elif op == "le":
            expr = [
                (
                    pl.when(pl.col(n).is_null() & pl.col(f"{n}{suffix}").is_null())
                    .then(pl.lit(True))
                    .otherwise(pl.col(n) <= pl.col(f"{n}{suffix}"))
                    .alias(n)
                )
                for n in materialized.columns
            ]
        else:
            raise ValueError(f"got unexpected comparison operator: {op}")

        return DataFrame(combined.select(expr), convert_dtypes=convert_dtypes, pydantic_model=self._pydantic_model)

    def __eq__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):  # type: ignore
        return self._perform_op("eq", other, convert_dtypes=False)

    def __ne__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):  # type: ignore
        return self._perform_op("ne", other, convert_dtypes=False)

    def __gt__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):
        return self._perform_op("gt", other, convert_dtypes=False)

    def __lt__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):
        return self._perform_op("lt", other, convert_dtypes=False)

    def __ge__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):
        return self._perform_op("ge", other, convert_dtypes=False)

    def __le__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]):
        return self._perform_op("le", other, convert_dtypes=False)

    def __add__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]) -> DataFrame:
        return self._perform_op(operator.add, other, convert_dtypes=True)

    def __sub__(self, other: Union[DataFrame, pl.DataFrame, pl.LazyFrame, pd.DataFrame, Any]) -> DataFrame:
        return self._perform_op(operator.sub, other, convert_dtypes=True)

    def __mul__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.mul, other, convert_dtypes=True)

    def __truediv__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.truediv, other, convert_dtypes=True)

    def __floordiv__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.floordiv, other, convert_dtypes=True)

    def __mod__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.mod, other, convert_dtypes=True)

    def __pow__(self, other: Union[int, float]) -> DataFrame:
        return self._perform_op(operator.pow, other, convert_dtypes=True)

    ############
    # Conversion
    ############
    def to_polars(self) -> pl.LazyFrame:
        """Get the underlying `DataFrame` as a `polars.LazyFrame`."""
        return self._underlying

    def to_pyarrow(self) -> pa.Table:
        materialized = self._materialize()
        pa_table = materialized.to_arrow()
        if self._convert_dtypes:
            pa_schema = pa.schema({k: Feature.from_root_fqn(k).converter.pyarrow_dtype for k in pa_table.column_names})
            pa_table = pa_table.cast(pa_schema)
        return pa_table

    def to_pandas(self) -> pd.DataFrame:
        """Get the underlying dataframe as a `pandas.DataFrame`."""
        if pd is None:
            raise missing_dependency_exception("chalkpy[pandas]")

        def types_mapper(dtype: pa.DataType):
            if dtype in (pa.utf8(), pa.large_utf8()):
                return pd.StringDtype("python")
            return None

        pd_dataframe = self._materialize().to_pandas(types_mapper=types_mapper)
        # For pandas, the columns should be the Features, not the root fqns
        # So, convert the columns to object types, and then set them to the features
        pd_dataframe.columns = pd_dataframe.columns.astype("object")
        pd_dataframe = pd_dataframe.rename(columns={x.root_fqn: x for x in self.columns})
        return pd_dataframe

    def to_features(self) -> Sequence[Features]:
        """Get values in the dataframe as `Features` instances."""
        from chalk.features.feature_set import FeatureSetBase

        if self.namespace is None:
            raise ValueError("This method is not supported if the DataFrame spans multiple namespaces")
        ans: List[Features] = []
        for row in self.to_pyarrow().to_pylist():
            rooted_prefix_to_values: Dict[str, Dict[str, Any]] = {}

            for k, v in row.items():
                rooted_prefix_split = k.split(".")[:-1]
                for i in range(1, len(rooted_prefix_split) + 1):
                    rooted_prefix = ".".join(rooted_prefix_split[:i])
                    if rooted_prefix not in rooted_prefix_to_values:
                        rooted_prefix_to_values[rooted_prefix] = {}
                rooted_prefix_to_values[".".join(rooted_prefix_split)][k] = v
            # Sorting in reverse to construct the innermost features first
            sorted_sub_features = sorted(rooted_prefix_to_values.keys(), key=lambda x: len(x), reverse=True)

            for rooted_prefix in sorted_sub_features:
                values = rooted_prefix_to_values[rooted_prefix]
                sub_kwargs: Dict[str, Any] = {}
                for k, v in values.items():
                    feature = Feature.from_root_fqn(k)
                    assert not feature.is_has_many, "has-many features are not supported recursively within a dataframe"
                    if feature.is_has_one:
                        sub_kwargs[feature.attribute_name] = v
                    else:
                        sub_kwargs[feature.attribute_name] = feature.converter.from_primitive_to_rich(v)
                if rooted_prefix == self.namespace:
                    features_cls = FeatureSetBase.registry[self.namespace]
                    ans.append(features_cls(**sub_kwargs))
                else:
                    rooted_prefix_split = rooted_prefix.split(".")
                    features_cls = Feature.from_root_fqn(rooted_prefix).joined_class
                    assert features_cls is not None
                    parent_rooted_prefix, feature_name = ".".join(rooted_prefix_split[:-1]), rooted_prefix_split[-1]
                    del feature_name  # unused
                    rooted_prefix_to_values[parent_rooted_prefix][rooted_prefix] = features_cls(**sub_kwargs)
        return ans

    #######################
    # Filtering / Selecting
    #######################
    def __getitem__(self, item: Any) -> DataFrame:
        """Filter by rows or by columns.

        Parameters
        ----------
        item

        Returns
        -------

        """
        has_bool_or_filter_value = any(isinstance(x, (bool, Filter)) for x in ensure_tuple(item))
        if has_bool_or_filter_value:
            # If we have a boolean or Filter value, then that means we need to ast-parse the caller since
            # python has already evaluated AND, OR, and IN operations into literal booleans or Filters
            # Skipping the parsing unless if we have need to for efficiency and to eliminate conflicts
            # with pytest
            from chalk.df.ast_parser import parse_dataframe_getitem

            item = parse_dataframe_getitem()
        if any(isinstance(x, (FeatureWrapper, Feature, Filter)) for x in ensure_tuple(item)):
            return DataFrame(
                filter_data_frame(item, namespace=self.namespace, underlying=self._underlying),
                pydantic_model=self._pydantic_model,
            )
        else:
            # Otherwise, use the standard polars selection format
            # Must materialize the dataframe to use __getitem__
            materialized = self._materialize()
            df = materialized[item]
            return DataFrame(df, pydantic_model=self._pydantic_model)

    def slice(self, offset: int = 0, length: Optional[int] = None) -> DataFrame:
        """Slice the `DataFrame`.

        Parameters
        ----------
        offset
            The offset to start at.
        length
            The number of rows in the slice. If None (the default), include all rows from `offset`
            to the end of the `DataFrame`.

        Returns
        -------
        DataFrame
            The dataframe with the slice applied.
        """
        return DataFrame(self._underlying.slice(offset, length))


# Hack to get VSCode/Pylance/Pyright to type DataFrame as Type[DataFrameImpl]
# but IntelliJ to type it as Type[Any]
# Vscode can parse through literal dicts; IntelliJ can't
_dummy_dict = {"0": DataFrameImpl}

DataFrame = _dummy_dict["0"]
