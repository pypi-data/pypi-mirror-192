from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, Any, Union

from pydantic import BaseModel, Field, ValidationError, validator

from ..utils import from_dt_f_to_human, from_dt_f_to_regexp

if TYPE_CHECKING:
    from pydantic.types import ModelOrDc

_DEFAULT_DATES_FORMAT = "%Y-%m-%d"
DATES_FORMAT = _DEFAULT_DATES_FORMAT


def _validate_datetime(cls: "ModelOrDc", dt: datetime) -> datetime:
    """Validate datetime value being more than datetime.now().

    Args:
        cls (ModelOrDc): Model class
        dt (datetime): datetime.datetime value to validate

    Raises:
        ValidationError: on validation error

    Returns:
        datetime: validated datetime.datetime value
    """
    if dt > datetime.now():
        raise ValidationError(f"{dt} more than now", cls)
    return dt


class BaseDateRangeConfigField(BaseModel, ABC):
    """Abstract datetime range model that specifies mandatory constant field date_range_type."""

    date_range_type: str = Field(
        "custom_date",
        const=True,
        order=2,
    )


class CustomDateRange(BaseDateRangeConfigField):
    """Model describes datetime range from start date to end date."""

    class Config:
        """CustomDateRange model config."""

        title = "Custom Date Range"

    date_from: datetime = Field(
        title="Start Date",
        description=f"Start date in format {from_dt_f_to_human(DATES_FORMAT)}",
        examples=[datetime.strftime(datetime.now(), DATES_FORMAT)],
        pattern=from_dt_f_to_regexp(DATES_FORMAT),
        order=0,
        validator=_validate_datetime,
    )
    date_to: datetime = Field(
        title="End Date",
        description=f"End date in format {from_dt_f_to_human(DATES_FORMAT)}",
        examples=[datetime.strftime(datetime.now(), DATES_FORMAT)],
        pattern=from_dt_f_to_regexp(DATES_FORMAT),
        order=1,
        validator=_validate_datetime,
    )
    date_range_type: str = Field(
        "custom_date",
        const=True,
        order=2,
    )


class LastDaysCountDateRange(BaseDateRangeConfigField):
    """Model describes datetime range within last days count."""

    class Config:
        """LastDaysCountDateRange model config."""

        title = "Custom Date Range"

    last_days_count: int = Field(
        title="Last Days Count",
        description="Count of last days to replicate",
        minimum=0,
        maximum=3650,
        examples=[30],
        order=0,
    )
    should_load_today: bool = Field(
        title="Load Today?",
        description="Should connector load today time as End Time? If not, End Time will be yesterday.",
        order=1,
        default=False,
    )
    date_range_type: str = Field(
        "last_n_days",
        const=True,
        order=2,
    )


class FromStartDayToTodayDateRange(BaseDateRangeConfigField):
    """Model describes datetime range from specific start date to today.

    should_load_today field is optional - if True, load up to today (derives from datetime.now()),
    if False - up to yesterday.
    """

    class Config:
        """FromStartDayToTodayDateRange model config."""

        title = "Custom Date Range"

    date_from: datetime = Field(
        title="Start Date",
        description=f"Start date in format {from_dt_f_to_human(DATES_FORMAT)}",
        examples=[datetime.strftime(datetime.now(), DATES_FORMAT)],
        pattern=from_dt_f_to_regexp(DATES_FORMAT),
        order=0,
        validator=_validate_datetime,
    )
    should_load_today: bool = Field(
        title="Load Today?",
        description="Should connector load today time as End Time? If not, End Time will be yesterday.",
        order=1,
        default=False,
    )
    date_range_type: str = Field(
        "custom_date",
        const=True,
        order=2,
    )


class BaseDateRangeConnectorConfig(BaseModel):
    date_range: Union[
        CustomDateRange, LastDaysCountDateRange, FromStartDayToTodayDateRange
    ] = Field(
        title="Date Range",
        description="Choose date period that must be loaded",
    )

    @staticmethod
    def _change_format_to_oneOf(schema: dict, props_to_change: list[str]) -> dict:
        for prop in props_to_change:
            schema["properties"][prop]["type"] = "object"
            if "oneOf" in schema["properties"][prop]:
                continue
            schema["properties"][prop]["oneOf"] = schema["properties"][prop].pop(
                "anyOf"
            )
        return schema

    @classmethod
    def schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Override the schema classmethod to enable some post-processing."""
        props_to_change = ["date_range"]
        schema = super().schema(*args, **kwargs)
        schema = cls._change_format_to_oneOf(schema, props_to_change)
        return schema
