from typing import TypedDict

from proexe.dynamic_tables.domain.ports.dynamic_field_repository import DynamicFieldRepository
from proexe.dynamic_tables.domain.ports.dynamic_table_builder import DynamicTableBuilder
from proexe.dynamic_tables.domain.ports.dynamic_table_repository import DynamicTableRepository
from proexe.dynamic_tables.domain.ports.schema_editor import SchemaEditor
from proexe.dynamic_tables.models import DynamicField, DynamicTable, DynamicTableProtocol
from proexe.users.types import UserProtocol


class FieldTypedDict(TypedDict):
    name: str
    type: str


class CreateDynamicTableUseCase:
    def __init__(
        self,
        dynamic_table_builder: DynamicTableBuilder,
        schema_editor: SchemaEditor,
        dynamic_table_repository: DynamicTableRepository,
        dynamic_field_repository: DynamicFieldRepository,
    ) -> None:
        self._dynamic_table_builder = dynamic_table_builder
        self._schema_editor = schema_editor
        self._dynamic_table_repository = dynamic_table_repository
        self._dynamic_field_repository = dynamic_field_repository

    def execute(
        self, *, name: str, fields: list[FieldTypedDict], user: UserProtocol, description: str | None = None
    ) -> DynamicTableProtocol:
        dynamic_table = DynamicTable(name=name, description=description, user=user)
        self._dynamic_table_repository.save(dynamic_table=dynamic_table)

        dynamic_fields = [
            DynamicField(name=field["name"], type=field["type"], dynamic_table=dynamic_table) for field in fields
        ]

        self._dynamic_field_repository.save_many(dynamic_fields)

        table = self._dynamic_table_builder.build(dynamic_table=dynamic_table)

        self._schema_editor.create_table(table=table)

        return dynamic_table
