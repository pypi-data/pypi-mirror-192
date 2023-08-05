from abc import ABC, abstractmethod, classmethod
from typing import Any, Literal

from pydantic import BaseModel, Field


class OneOfConfigAbstractChildBase(BaseModel, ABC):
    @property
    @classmethod
    @abstractmethod
    def const_field_name(self) -> str:
        pass

    def __init_subclass__(cls) -> None:
        field = cls.__fields__.get(cls.const_field_name)
        assert (
            field
        ), f"Field {cls.const_field_name} is abstract and must be redefined in class {cls.__name__}"
        assert field.type_ == str and getattr(
            field.field_info, "const", False
        ), f"Field {field} type must be `str` typed `Field` with `const=True`. "
        f"Define it like so: `{field}: str = Field('some_const_value', const=True)`"
