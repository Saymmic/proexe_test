from typing import Protocol

from proexe.dynamic_tables.types import DynamicTableProtocol


class SchemaEditor(Protocol):
    def create_table(self, table: DynamicTableProtocol) -> None:
        pass
