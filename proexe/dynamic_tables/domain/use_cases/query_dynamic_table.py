from uuid import UUID


class QueryDynamicTableUseCase:
    def __init__(self, dynamic_table_repository) -> None:
        self._dynamic_table_repository = dynamic_table_repository

    def execute(self, *, dynamic_table_id: str | UUID) -> None:
        pass
