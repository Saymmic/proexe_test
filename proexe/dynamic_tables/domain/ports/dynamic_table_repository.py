from typing import Protocol

from proexe.dynamic_tables.types import DynamicTableProtocol


class DynamicTableRepository(Protocol):
    def save(self, dynamic_table: DynamicTableProtocol) -> None:
        ...
