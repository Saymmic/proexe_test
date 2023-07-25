from proexe.dynamic_tables.domain.ports.schema_editor import SchemaEditor
from proexe.dynamic_tables.types import DynamicTableProtocol


class DjangoSchemaEditor(SchemaEditor):
    def __init__(self, connection):  # TODO: Annotate
        self._connection = connection

    def create_table(self, table: DynamicTableProtocol) -> None:
        with self._connection.schema_editor() as schema_editor:
            schema_editor.create_model(table)
