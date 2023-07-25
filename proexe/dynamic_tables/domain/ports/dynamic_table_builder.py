from typing import Any, Protocol

from proexe.dynamic_tables.types import DynamicTableProtocol


class DynamicTableBuilder(Protocol):
    def build(self, dynamic_table: DynamicTableProtocol) -> Any:
        pass
