from functools import cache
from typing import Any

from django.db import connections
from django.db.models import QuerySet

from proexe.dynamic_tables.builders import DynamicFieldsBuilder, DynamicTableModelBuilder
from proexe.dynamic_tables.builders.dynamic_table_builder import TableDTO
from proexe.dynamic_tables.builders.dynamic_table_serializer_builder import DynamicTableSerializerBuilder
from proexe.dynamic_tables.models import Field, Table
from proexe.dynamic_tables.types import DjangoModelFieldType, DjangoModelSerializerType, DjangoModelType, FieldDataType
from proexe.users.models import User


class DynamicTableService:
    def __init__(
        self,
        dynamic_table_model_builder: DynamicTableModelBuilder,
        dynamic_field_builder: DynamicFieldsBuilder,
        dynamic_table_serializer_builder: DynamicTableSerializerBuilder,
    ):
        self._dynamic_field_builder = dynamic_field_builder
        self._dynamic_table_model_builder = dynamic_table_model_builder
        self._dynamic_table_serializer_builder = dynamic_table_serializer_builder

    @cache
    def _get_dynamic_table_model(self, table: Table) -> DjangoModelType:
        table_dto = TableDTO(name=table.name, meta=table.meta, username=table.user.username, fields=table.fields.all())

        return self._dynamic_table_model_builder.build(table=table_dto)

    def create(self, table: Table) -> type[DjangoModelType]:
        connection = connections["default"]
        dynamic_table_model = self._get_dynamic_table_model(table=table)

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(dynamic_table_model)

        return dynamic_table_model

    def update(
        self,
        old_table: Table,
        new_table: Table,
        name: str,
        fields_to_alter: list[Field],
        fields_to_delete: list[Field],
        fields_to_create: list[Field],
        # fields,
    ) -> None:
        old = self._dynamic_table_model
        self.update_dynamic_model_table(old_table, new_table)
        # fields_to_alter = self._dynamic_field_builder.build(fields_to_alter)
        # fields_to_create = self._dynamic_field_builder.build(fields_to_create)
        # fields_to_delete = self._dynamic_field_builder.build(fields_to_delete)
        #
        # print(f"fields_to_alter: {fields_to_alter}")
        # print(f"fields_to_create: {fields_to_create}")
        # print(f"fields_to_delete: {fields_to_delete}")
        #
        # connection = connections["default"]
        # with connection.schema_editor() as schema_editor:
        #     if old_table.name != name:
        #         schema_editor.alter_db_table(self._dynamic_table_model, old_table.name, name)
        #
        #     for field_name in fields_to_delete.keys():
        #         schema_editor.remove_field(
        #             self._dynamic_table_model, self._dynamic_table_model._meta.get_field(field_name)
        #         )
        #     for field in fields_to_alter.values():
        #         old_field = Field.objects.get(pk=field.pk)
        #         schema_editor.alter_field(self._dynamic_table_model, old_field, field)
        #     for field in fields_to_create.values():
        #         schema_editor.add_field(self._dynamic_table_model, field)

    def update_dynamic_model_table(
        self,
        table: Table,
        fields_to_alter: list[DjangoModelFieldType],
        fields_to_remove: list[DjangoModelFieldType],
        fields_to_create: list[DjangoModelFieldType],
        new_table_name: str | None = None,
    ):
        connection = connections["default"]
        dynamic_table_model = self._get_dynamic_table_model(table=table)

        for field in fields_to_remove:
            django_field = dynamic_table_model._meta.get_field(field.name)

            with connection.schema_editor() as schema_editor:
                schema_editor.remove_field(dynamic_table_model, django_field)

        for field in fields_to_create:
            django_field = self._dynamic_field_builder.build(fields=[field])[field.name]
            dynamic_table_model.add_to_class(field.name, django_field)

            with connection.schema_editor() as schema_editor:
                schema_editor.add_field(dynamic_table_model, django_field)

        for field in fields_to_alter:
            new_django_field = self._dynamic_field_builder.build(field)
            old_django_field = dynamic_table_model._meta.get_field(field.name)

            with connection.schema_editor() as schema_editor:
                schema_editor.alter_field(dynamic_table_model, old_django_field, new_django_field)

        if new_table_name:
            with connection.schema_editor() as schema_editor:
                schema_editor.alter_db_table(
                    dynamic_table_model,
                    dynamic_table_model._meta.db_table,
                    self._dynamic_table_model_builder._build_name(
                        table=TableDTO(name=new_table_name, meta={}, username=table.user.username, fields=[])
                    ),
                )

    def query_all(self, table: Table) -> QuerySet[DjangoModelType]:
        dynamic_table_model = self._get_dynamic_table_model(table=table)

        return dynamic_table_model.objects.all()

    def create_row(self, table: Table, data: dict[str, Any]) -> DjangoModelType:
        dynamic_table_model = self._get_dynamic_table_model(table=table)

        return dynamic_table_model.objects.create(**data)

    def get_serializer_class(self, table: Table) -> type[DjangoModelSerializerType]:
        dynamic_table_model = self._get_dynamic_table_model(table=table)
        dynamic_table_model_serializer = self._dynamic_table_serializer_builder.build(
            dynamic_table_model=dynamic_table_model
        )

        return dynamic_table_model_serializer


class TableService:
    def __init__(self, dynamic_table_service: DynamicTableService) -> None:
        self._dynamic_table_service = dynamic_table_service

    def create(self, name: str, fields: list[FieldDataType], user: User) -> Table:
        table = Table(name=name, user=user)
        table.full_clean()
        table.save()

        fields = [Field(name=f["name"], type=f["type"], table=table) for f in fields]
        Field.objects.bulk_create(fields)

        self._dynamic_table_service.create(table=table)

        return table

    def update(self, table: Table, name: str, fields: list[FieldDataType], user) -> Table:
        fields_to_alter = [
            Field(uuid="uuid", name=f["name"], type=f["type"], table=table)
            for f in fields
            if f.get("uuid") is not None
        ]
        fields_to_create = [
            Field(name=f["name"], type=f["type"], table=table) for f in fields if f.get("uuid") is None
        ]
        fields_to_remove = table.fields.exclude(uuid__in=[f.uuid for f in fields_to_alter])

        self._dynamic_table_service.update_dynamic_model_table(
            table=table,
            new_table_name=name if name != table.name else None,
            fields_to_alter=fields_to_alter,
            fields_to_remove=fields_to_remove,
            fields_to_create=fields_to_create,
        )
        if fields_to_alter:
            Field.objects.bulk_update(fields_to_alter)
        if fields_to_remove:
            Field.objects.filter(uuid__in=fields_to_remove).delete()
        if fields_to_create:
            Field.objects.bulk_create(fields_to_create)

        table.name = name
        table.full_clean()
        table.save()
        # table.refresh_from_db()

        return table
