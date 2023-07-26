from proexe.dynamic_tables.domain.ports.dynamic_table_repository import DynamicTableRepository
from proexe.dynamic_tables.types import DynamicTableProtocol


class DjangoDynamicTableRepository(DynamicTableRepository):
    def save(self, dynamic_table: DynamicTableProtocol) -> None:
        dynamic_table.save()
