from __future__ import annotations

from typing import TYPE_CHECKING, Type

from django.db import connections, models

if TYPE_CHECKING:
    from proexe.dynamic_tables.models import DynamicTable


class DynamicTableManager(models.Manager):
    def build_dynamic_table_model(self, dynamic_table: DynamicTable) -> Type[models.Model]:
        from proexe.dynamic_tables.builders import DynamicFieldsBuilder, DynamicTableModelBuilder

        _table_builder = DynamicTableModelBuilder(field_builder=DynamicFieldsBuilder())

        model = _table_builder.build(dynamic_table)

        return model

    def create_dynamic_table_in_db(self, dynamic_table: DynamicTable) -> Type[models.Model]:
        model = self.build_dynamic_table_model(dynamic_table)

        connection = connections["default"]

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)

        return model

    def update_dynamic_table_in_db(
        self, dynamic_table: DynamicTable, new_dynamic_table: DynamicTable
    ) -> Type[models.Model]:
        connection = connections["default"]

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(dynamic_table.dynamic_table_model)
            schema_editor.create_model(new_dynamic_table.dynamic_table_model)

        return new_dynamic_table.dynamic_table_model


class DynamicFieldManager(models.Manager):
    pass
