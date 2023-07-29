from dataclasses import dataclass
from typing import Type

from django.db import models

from proexe.dynamic_tables.builders.dynamic_field_builder import DynamicFieldsBuilder, FieldDTO
from proexe.dynamic_tables.types import DjangoModelType


@dataclass
class TableDTO:
    name: str
    meta: dict
    username: str
    fields: list[FieldDTO]


class DynamicTableModelBuilder:
    """
    Builder design pattern
    """

    def __init__(self, field_builder: DynamicFieldsBuilder) -> None:
        self._field_builder = field_builder

    def _build_name(self, table: TableDTO) -> str:
        """
        Use the user as a namespace to avoid name collisions.
        """
        return f"{table.username}_{table.name}"

    def _build_fields(self, table: TableDTO) -> dict[str, models.Field]:
        return self._field_builder.build(table.fields)

    def _build_meta(self, dynamic_tabel: TableDTO) -> Type:
        class Meta:
            pass

        for key, value in dynamic_tabel.meta.items():
            setattr(Meta, key, value)

        return Meta

    def build(self, table: TableDTO) -> type[DjangoModelType]:
        name = self._build_name(table)
        fields = self._build_fields(table)
        meta = self._build_meta(table)

        model: type[DjangoModelType] = type(
            name, (models.Model,), {"__module__": "proexe.dynamic_tables.models", "Meta": meta, **fields}
        )  # noqa

        return model
