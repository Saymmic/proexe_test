from typing import Protocol

from proexe.dynamic_tables.types import DynamicFieldProtocol


class DynamicFieldRepository(Protocol):
    def save_many(self, dynamic_fields: list[DynamicFieldProtocol]) -> None:
        ...
