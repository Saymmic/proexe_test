from typing import Type

from django.db import models

from proexe.dynamic_tables.builders.dynamic_field_builder import DynamicFieldsBuilder
from proexe.dynamic_tables.models import Table
from proexe.dynamic_tables.types import DjangoModelType


class DynamicTableModelBuilder:
    """
    Builder design pattern
    """

    def __init__(self, field_builder: DynamicFieldsBuilder) -> None:
        self._field_builder = field_builder

    def _build_name(self, table: Table) -> str:
        """
        Use the user as a namespace to avoid name collisions.
        """
        return f"{table.user.username}_{table.name}"

    def _build_fields(self, table: Table) -> dict[str, models.Field]:
        return self._field_builder.build(table.fields.all())

    def _build_meta(self, dynamic_tabel: Table) -> Type:
        class Meta:
            pass

        for key, value in dynamic_tabel.meta.items():
            setattr(Meta, key, value)

        return Meta

    def build(self, table: Table) -> type[DjangoModelType]:
        name = self._build_name(table)
        fields = self._build_fields(table)
        meta = self._build_meta(table)

        model: type[DjangoModelType] = type(
            name, (models.Model,), {"__module__": "proexe.dynamic_tables.models", "Meta": meta, **fields}
        )  # noqa

        return model
