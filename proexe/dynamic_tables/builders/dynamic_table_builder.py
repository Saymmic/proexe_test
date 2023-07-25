from typing import Type

from django.db import models

from proexe.dynamic_tables.builders.dynamic_field_builder import DynamicFieldsBuilder
from proexe.dynamic_tables.models import DynamicTable


class DynamicTableModelBuilder:
    """
    Builder design pattern
    """

    def __init__(self, field_builder: DynamicFieldsBuilder) -> None:
        self._field_builder = field_builder

    def _build_name(self, dynamic_table: DynamicTable) -> str:
        """
        Use the user as a namespace to avoid name collisions.
        """
        return f"{dynamic_table.user.username}_{dynamic_table.name}"

    def _build_fields(self, dynamic_table: DynamicTable) -> dict[str, models.Field]:
        return self._field_builder.build(dynamic_table.dynamic_fields.all())

    def _build_meta(self, dynamic_tabel: DynamicTable) -> Type:
        class Meta:
            pass

        for key, value in dynamic_tabel.meta.items():
            setattr(Meta, key, value)

        return Meta

    def build(self, dynamic_table: DynamicTable) -> Type[models.Model]:
        name = self._build_name(dynamic_table)
        fields = self._build_fields(dynamic_table)
        meta = self._build_meta(dynamic_table)

        model: Type[models.Model] = type(
            name, (models.Model,), {"__module__": "proexe.dynamic_tables.models", "Meta": meta, **fields}
        )  # noqa

        return model
