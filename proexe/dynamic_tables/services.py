from typing import Any

from django.db import connections

from proexe.dynamic_tables.builders import DynamicFieldsBuilder, DynamicTableModelBuilder
from proexe.dynamic_tables.builders.dynamic_table_serializer_builder import DynamicTableSerializerBuilder
from proexe.dynamic_tables.models import Field, Table
from proexe.dynamic_tables.types import DjangoModelSerializerType, DjangoModelType
from proexe.users.models import User


class DynamicTableService:
    def __init__(
        self,
        table: Table,
    ):
        self._dynamic_table_model = DynamicTableModelBuilder(field_builder=DynamicFieldsBuilder()).build(table=table)
        self._dynamic_table_serializer_builder = DynamicTableSerializerBuilder()

    def create(self) -> type[DjangoModelType]:
        connection = connections["default"]

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self._dynamic_table_model)

        return self._dynamic_table_model

    def update(self) -> type[DjangoModelType]:
        # TODO: Implement
        pass

    def query_all(self) -> list[DjangoModelType]:
        return self._dynamic_table_model.objects.all()

    def create_row(self, data: dict[str, Any]) -> DjangoModelType:
        return self._dynamic_table_model.objects.create(**data)

    def get_serializer_class(self) -> type[DjangoModelSerializerType]:
        return self._dynamic_table_serializer_builder.build(dynamic_table_model=self._dynamic_table_model)


class TableService:
    def create(self, name: str, fields: list[dict[str, Field.Type]], user: User) -> Table:
        table = Table(name=name, user=user)
        table.full_clean()
        table.save()

        fields = [Field(name=f["name"], type=f["type"], table=table) for f in fields]
        Field.objects.bulk_create(fields)

        DynamicTableService(table=table).create()

        return table

    def update(self, table: Table) -> Table:
        pass
