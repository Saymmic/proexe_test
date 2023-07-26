from proexe.dynamic_tables.domain.ports.dynamic_field_repository import DynamicFieldRepository
from proexe.dynamic_tables.models import DynamicField
from proexe.dynamic_tables.types import DynamicFieldProtocol


class DjangoDynamicFieldRepository(DynamicFieldRepository):
    def save_many(self, dynamic_fields: list[DynamicFieldProtocol]) -> None:
        DynamicField.objects.bulk_create(dynamic_fields)
