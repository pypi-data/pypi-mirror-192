import dataclasses
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, List, Optional, Type

from chalk._monitoring.Chart import Chart
from chalk._monitoring.gql_conversion import convert_chart
from chalk._version import __version__
from chalk.config.project_config import load_project_config
from chalk.features import Feature, FeatureSetBase
from chalk.features.resolver import Resolver, SinkResolver, StreamResolver
from chalk.importer import FailedImport
from chalk.parsed._graph_validation import validate_graph
from chalk.parsed.duplicate_input_gql import (
    ChalkPYInfo,
    EnvironmentSettingsGQL,
    FeatureSettings,
    MetadataSettings,
    ProjectSettingsGQL,
    UpsertGraphGQL,
    ValidationSettings,
)
from chalk.parsed.json_conversions import convert_type_to_gql
from chalk.utils import paths


def _is_relative_to(x: Path, other: Path) -> bool:
    try:
        x.relative_to(other)
        return True
    except ValueError:
        return False


def get_registered_types_as_json(scope_to: Path, failed: List[FailedImport], indent: int = 2) -> str:
    features = [
        convert_type_to_gql(feature)
        for x in FeatureSetBase.registry.values()
        if x.__module__ in sys.modules and _is_relative_to(paths.get_classpath(x), scope_to)
        for feature in x.features
        if not feature.is_autogenerated and not feature.no_display
    ]
    stream_resolvers = [
        convert_type_to_gql(t) for t in StreamResolver.registry if _is_relative_to(Path(t.filename), scope_to)
    ]
    resolvers = [convert_type_to_gql(t) for t in Resolver.registry if _is_relative_to(Path(t.filename), scope_to)]
    sink_resolvers = [
        convert_type_to_gql(t) for t in SinkResolver.registry if _is_relative_to(Path(t.filename), scope_to)
    ]
    charts = [convert_chart(chart) for chart in Chart._registry]

    def read_packages(filename: str) -> Optional[List[str]]:
        reqs = list()
        try:
            with open(filename) as f:
                for r in f.readlines():
                    cleaned = re.sub("#.*", "", r).rstrip("\n").strip()
                    if cleaned != "":
                        reqs.append(cleaned)
            return reqs
        except OSError:
            return None

    config = load_project_config()
    if config is not None:
        config = ProjectSettingsGQL(
            project=config.project,
            environments=config.environments
            and [
                EnvironmentSettingsGQL(
                    id=i,
                    runtime=e.runtime,
                    requirements=e.requirements,
                    dockerfile=e.dockerfile,
                    requiresPackages=None
                    if e.requirements is None
                    else read_packages(
                        os.path.join(
                            os.path.dirname(config.local_path),
                            e.requirements,
                        )
                    ),
                )
                for i, e in config.environments.items()
            ],
            validation=ValidationSettings(
                feature=FeatureSettings(
                    metadata=[
                        MetadataSettings(name=m.name, missing=m.missing) for m in config.validation.feature.metadata
                    ]
                    if config.validation.feature.metadata
                    else None
                )
                if config.validation.feature
                else None
            )
            if config.validation
            else None,
        )

    graph = UpsertGraphGQL(
        streams=stream_resolvers,
        sinks=sink_resolvers,
        features=features,
        config=config,
        failed=failed,
        resolvers=resolvers,
        charts=charts,
        chalkpy=ChalkPYInfo(version=__version__),
    )
    errors = validate_graph(graph)
    graph.errors = errors
    return json.dumps(
        dataclasses.asdict(graph),
        indent=indent,
    )
