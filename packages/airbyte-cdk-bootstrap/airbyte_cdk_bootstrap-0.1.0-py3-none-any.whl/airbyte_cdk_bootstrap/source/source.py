import json
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import yaml
from airbyte_cdk.connector import load_optional_package_file
from airbyte_cdk.models import ConnectorSpecification, DestinationSyncMode
from airbyte_cdk.sources import AbstractSource as _AbstractSource

from ..utils import access_dict_key_or_create
from .models import SpecFormat
from .spec import BaseDateRangeConnectorConfig

if TYPE_CHECKING:
    from pydantic import BaseModel


class AbstractDateRangeSource(_AbstractSource, ABC):
    """
    airbyte_cdk.sources.Source extension.

    This extension supports dates field spawn in spec.
    """

    @property
    def spec_dates_order(cls) -> int:
        """
        Date range field order in connector spec.

        If none, order will be the last one.
        2 is default because usually it comes after auth field.
        """
        return 2

    @abstractmethod
    @property
    def spec_format(cls) -> SpecFormat:
        """
        Spec format. Accepts SpecFormat enum.

        - SpecFormat.SCHEMA_FILE for spec.yaml or spec.json
        - SpecFormat.PYDANTIC_MODEL for ConnectorConfig pydantic model
            specified in Source.pydantic_model property

        Must be overriden:
        >>> class ExampleSource(Source):
        >>>     spec_format = SpecFormat.PYDANTIC_MODEL
        """
        raise NotImplementedError

    @property
    def pydantic_spec_model(cls) -> BaseDateRangeConnectorConfig | None:
        """
        Date range field order in connector spec.

        If none, order will be the last one.
        2 is default because usually it comes after auth field.
        """
        return None

    @property
    def documentation_uri(cls) -> str | None:
        """Connector documentation URI used in connector spec."""
        return None

    @property
    def changelog_uri(cls) -> str | None:
        """Connector changelog URI used in connector spec."""
        return None

    @property
    def supports_incremental(cls) -> bool:
        """Does connector supports incremental."""
        return False

    @property
    def supported_destination_sync_modes(cls) -> list[DestinationSyncMode]:
        """List of destination sync modes that connector supports."""
        return [DestinationSyncMode.append]

    @abstractmethod
    @property
    def generate_spec_dates(cls) -> bool:
        """
        Generate date range field in connector config specofication or not.

        Must be overriden:
        >>> class ExampleSource(Source):
        >>>     generate_spec_dates = True
        """
        raise NotImplementedError

    def _get_obj_from_package_spec_file(self) -> dict[str, Any]:
        """
        Return the spec object for this integration in dict type.

        By default, this will be loaded from a "spec.yaml" or a "spec.json" in the package root.
        """
        package = self.__class__.__module__.split(".")[0]

        yaml_spec = load_optional_package_file(package, "spec.yaml")
        json_spec = load_optional_package_file(package, "spec.json")

        if yaml_spec and json_spec:
            raise RuntimeError(
                "Found multiple spec files in the package. Only one of spec.yaml or spec.json should be provided."
            )

        if yaml_spec:
            spec_obj = yaml.load(yaml_spec, Loader=yaml.SafeLoader)
        elif json_spec:
            try:
                spec_obj = json.loads(json_spec)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Could not read json spec file: {error}. Please ensure that it is a valid JSON."
                )
        else:
            raise FileNotFoundError(
                "Unable to find spec.yaml or spec.json in the package."
            )

        return spec_obj

    def _spawn_datetime_range_field_in_file_spec_obj(
        self, spec: ConnectorSpecification
    ):
        spec_config: dict[str, Any] = spec.connectionSpecification
        spec_fields_to_update: list[tuple[str, Any]] = [
            ("properties", []),
            ("definitions", []),
        ]
        base_config_schema = BaseDateRangeConnectorConfig.schema()

        for field_name, default_value in spec_fields_to_update:
            original_field: dict[str, Any] = access_dict_key_or_create(
                spec_config, field_name, default_value
            )
            original_field.update(base_config_schema[field_name])

        required_fields: list[str] = access_dict_key_or_create(
            spec_config, "required", []
        )
        required_fields += base_config_schema["required"]
        return spec

    def _load_spec_from_schema_file(self) -> ConnectorSpecification:
        spec_obj = self._get_obj_from_package_spec_file()
        spec: ConnectorSpecification = ConnectorSpecification.parse_obj(spec_obj)
        if self.generate_spec_dates:
            spec = self._spawn_datetime_range_field_in_file_spec_obj(spec)

        return spec

    def _make_spec_from_pydantic_model(self) -> ConnectorSpecification:
        if not isinstance(self.pydantic_spec_model, BaseModel):
            raise ValueError(
                "Source.pydantic_model is not instance of pydantic.BaseModel."
            )
        return ConnectorSpecification(
            documentationUrl=self.documentation_uri,
            changelogUrl=self.changelog_uri,
            supportsIncremental=self.supports_incremental,
            supported_destination_sync_modes=self.supported_destination_sync_modes,
            connectionSpecification=self.pydantic_spec_model.schema(),
        )

    def spec(self, logger: logging.Logger) -> ConnectorSpecification:
        """Return spec as ConnectorSpecification object.

        It's describing required configurations (e.g: username and password) required to
        run this integration.
        """
        if self.spec_format == SpecFormat.SCHEMA_FILE:
            spec = self._load_spec_from_schema_file()
        elif self.spec_format == SpecFormat.PYDANTIC_MODEL:
            spec = self._make_spec_from_pydantic_model()
        else:
            raise ValueError(f"Source.SPEC_FORMAT must be one of: {list(SpecFormat)}")
        return spec
