import json

import pytest
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from proexe.dynamic_tables.builders import DynamicFieldsBuilder, DynamicTableModelBuilder
from proexe.dynamic_tables.builders.dynamic_table_serializer_builder import DynamicTableSerializerBuilder
from proexe.dynamic_tables.models import Field, Table
from proexe.dynamic_tables.services import DynamicTableService, TableService
from proexe.users.models import User

# Normally I would use factoryboy and pytests fixtures but for simplicity I will create objects in tests


class TestDynamicTableView:
    def test_post_table_created(self, db, api_client: APIClient) -> None:
        # Given
        create_data = {
            "name": "test_table",
            "fields": [
                {"name": "test_string", "type": "STRING"},
                {"name": "test_number", "type": "NUMBER"},
                {"name": "test_bool", "type": "BOOLEAN"},
            ],
        }

        # When
        response = api_client.post(reverse("api:tables:create"), create_data, format="json")

        # Then
        assert response.status_code == 201
        assert response.data["name"] == create_data["name"]
        assert len(response.data["fields"]) == len(create_data["fields"])
        assert json.dumps(response.data["fields"]) == json.dumps(create_data["fields"])

        assert Table.objects.count() == 1

        table = Table.objects.get(uuid=response.data["uuid"])

        assert table is not None

    def test_table_name_too_long(self, db, api_client: APIClient) -> None:
        # Given
        create_data = {
            "name": "test_table" * 10,
            "fields": [
                {"name": "test_string", "type": "STRING"},
                {"name": "test_number", "type": "NUMBER"},
                {"name": "test_bool", "type": "BOOLEAN"},
            ],
        }

        # When
        response = api_client.post(reverse("api:tables:create"), create_data, format="json")

        # Then
        assert response.status_code == 400
        assert response.data == {
            "message": "Validation error",
            "extra": {
                "fields": {
                    "name": [
                        ErrorDetail(string="Ensure this field has no more than 38 characters.", code="max_length")
                    ]
                }
            },
        }

    def test_update_table(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        table = Table.objects.create(name="test_table", user=api_test_user)
        altered_field = Field(name="altered_test_string", type="STRING", table=table)
        deleted_field = Field(name="test_number", type="NUMBER", table=table)
        new_field = Field(name="test_bool", type="BOOLEAN", table=table)
        fields = [
            altered_field,
            deleted_field,
        ]
        Field.objects.bulk_create(fields)
        dynamic_table_service = DynamicTableService(
            dynamic_field_builder=DynamicFieldsBuilder(),
            dynamic_table_model_builder=DynamicTableModelBuilder(
                field_builder=DynamicFieldsBuilder(),
            ),
            dynamic_table_serializer_builder=DynamicTableSerializerBuilder(),
        )
        dynamic_table_service.create(table=table)

        altered_field_new_name = "another_test_string"
        update_data = {
            "name": "test_table",
            "fields": [
                {"uuid": str(altered_field.uuid), "name": altered_field_new_name, "type": "STRING"},
                {"name": new_field.name, "type": new_field.type},
            ],
        }

        # When
        print(update_data)
        response = api_client.put(reverse("api:tables:update", kwargs={"pk": table.uuid}), update_data, format="json")
        print(response.data)

        # Then
        assert response.status_code == 200
        assert response.data["name"] == update_data["name"]
        assert len(response.data["fields"]) == len(update_data["fields"])
        assert response.data["fields"][0]["name"] == update_data["fields"][0]["name"]
        assert response.data["fields"][0]["type"] == update_data["fields"][0]["type"]
        assert response.data["fields"][1]["name"] == update_data["fields"][1]["name"]
        assert response.data["fields"][1]["type"] == update_data["fields"][1]["type"]

        assert Table.objects.count() == 1

        table = Table.objects.get(uuid=response.data["uuid"])

        # Check if table exists and the structure was updated
        print(table)
        data = {altered_field_new_name: "some_value", new_field.name: True}
        print(data)
        dynamic_table_service.create_row(table=table, data=data)
        assert dynamic_table_service.query_all(table=table).count() == 1

    def test_creating_data_in_dynamic_table(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        table = Table.objects.create(name="test_table", user=api_test_user)
        fields = [
            Field(name="test_string", type="STRING", table=table),
            Field(name="test_number", type="NUMBER", table=table),
            Field(name="test_bool", type="BOOLEAN", table=table),
        ]
        Field.objects.bulk_create(fields)
        dynamic_table_service = DynamicTableService(table=table)
        dynamic_table_service.create()

        create_dynamic_tale_row_data = {
            "test_string": "test",
            "test_number": 1,
            "test_bool": True,
        }

        # When
        response = api_client.post(
            reverse("api:tables:create_row", kwargs={"pk": table.pk}),
            data=create_dynamic_tale_row_data,
            format="json",
        )

        # Then
        assert response.status_code == 201
        assert dynamic_table_service.query_all().count() == 1
        assert response.data["test_string"] == create_dynamic_tale_row_data["test_string"]
        assert response.data["test_number"] == create_dynamic_tale_row_data["test_number"]
        assert response.data["test_bool"] == create_dynamic_tale_row_data["test_bool"]

    def test_table_respects_schema(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        table = Table.objects.create(name="test_table", user=api_test_user)
        fields = [
            Field(name="test_string", type="STRING", table=table),
            Field(name="test_number", type="NUMBER", table=table),
            Field(name="test_bool", type="BOOLEAN", table=table),
        ]
        Field.objects.bulk_create(fields)
        dynamic_table_service = DynamicTableService(table=table)
        dynamic_table_service.create()

        create_dynamic_tale_row_data = {
            "test_string": "test",
            "test_number": 1,
            "bad_field": True,
        }

        # When
        response = api_client.post(
            reverse("api:tables:create_row", kwargs={"pk": table.pk}),
            data=create_dynamic_tale_row_data,
            format="json",
        )

        # Then
        assert response.status_code == 400
        assert dynamic_table_service.query_all().count() == 0

    def test_get_data_from_table(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        table = Table.objects.create(name="test_table", user=api_test_user)
        fields = [
            Field(name="test_string", type="STRING", table=table),
            Field(name="test_number", type="NUMBER", table=table),
            Field(name="test_bool", type="BOOLEAN", table=table),
        ]
        Field.objects.bulk_create(fields)
        dynamic_table_service = DynamicTableService(table=table)
        dynamic_table_service.create()

        table_object_one = dynamic_table_service.create_row(
            data={"test_string": "test", "test_number": 1, "test_bool": True}
        )
        table_object_two = dynamic_table_service.create_row(
            data={"test_string": "test_2", "test_number": 2, "test_bool": False}
        )

        # When
        response = api_client.get(reverse("api:tables:list_rows", kwargs={"pk": table.pk}), format="json")

        # Then
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["test_string"] == table_object_one.test_string
        assert response.data[0]["test_number"] == table_object_one.test_number
        assert response.data[0]["test_bool"] == table_object_one.test_bool
        assert response.data[1]["test_string"] == table_object_two.test_string
        assert response.data[1]["test_number"] == table_object_two.test_number
        assert response.data[1]["test_bool"] == table_object_two.test_bool
