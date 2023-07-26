from uuid import UUID


class UpdateDynamicTableUseCase:
    def execute(self, *, uuid: UUID, name: str, fields: dict[str, Any], description: str | None = None) -> None:
        pass
