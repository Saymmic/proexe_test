import json

from django.urls import reverse
from rest_framework.test import APIClient

from proexe.dynamic_tables.models import DynamicField, DynamicTable
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
        response = api_client.post(reverse("api:dynamictable-list"), create_data, format="json")

        # Then
        assert response.status_code == 201
        assert response.data["name"] == create_data["name"]
        assert len(response.data["fields"]) == len(create_data["fields"])
        assert json.dumps(response.data["fields"]) == json.dumps(create_data["fields"])

        assert DynamicTable.objects.count() == 1

        dynamic_table = DynamicTable.objects.get(uuid=response.data["uuid"])

        # Check if table exists and its querable
        dynamic_table.dynamic_table_model.objects.create(test_string="test", test_number=1, test_bool=True)
        assert dynamic_table.dynamic_table_model.objects.count() == 1

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
        response = api_client.post(reverse("api:dynamictable-list"), create_data, format="json")

        # Then
        assert response.status_code == 400
        assert response.data["name"][0].code == "max_length"

    def test_update_dynamic_table(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        dynamic_table = DynamicTable.objects.create(name="test_table", user=api_test_user)
        dynamic_fields = [
            DynamicField(name="test_string", type="STRING", dynamic_table=dynamic_table),
            DynamicField(name="test_number", type="NUMBER", dynamic_table=dynamic_table),
            DynamicField(name="test_bool", type="BOOLEAN", dynamic_table=dynamic_table),
        ]
        DynamicField.objects.bulk_create(dynamic_fields)
        dynamic_table.create_dynamic_table_in_db()

        update_data = {
            "name": "another_test_table",
            "fields": [
                {"name": "another_test_string", "type": "STRING"},
                {"name": "another_test_number", "type": "NUMBER"},
                {"name": "another_test_bool", "type": "BOOLEAN"},
            ],
        }

        # When
        response = api_client.put(
            reverse("api:dynamictable-detail", kwargs={"pk": dynamic_table.uuid}), update_data, format="json"
        )

        # Then
        assert response.status_code == 200
        assert response.data["name"] == update_data["name"]
        assert len(response.data["fields"]) == len(update_data["fields"])
        assert json.dumps(response.data["fields"]) == json.dumps(update_data["fields"])

        assert DynamicTable.objects.count() == 1

        dynamic_table = DynamicTable.objects.get(uuid=response.data["uuid"])

        # Check if table exists and its querable
        dynamic_table.dynamic_table_model.objects.create(
            another_test_string="test", another_test_number=1, another_test_bool=True
        )
        assert dynamic_table.dynamic_table_model.objects.count() == 1

    def test_creating_data_in_dynamic_table(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        dynamic_table = DynamicTable.objects.create(name="test_table", user=api_test_user)
        dynamic_fields = [
            DynamicField(name="test_string", type="STRING", dynamic_table=dynamic_table),
            DynamicField(name="test_number", type="NUMBER", dynamic_table=dynamic_table),
            DynamicField(name="test_bool", type="BOOLEAN", dynamic_table=dynamic_table),
        ]
        DynamicField.objects.bulk_create(dynamic_fields)
        dynamic_table.create_dynamic_table_in_db()

        create_dynamic_tale_row_data = {
            "test_string": "test",
            "test_number": 1,
            "test_bool": True,
        }

        # When
        response = api_client.post(
            reverse("api:dynamictable-row", kwargs={"pk": dynamic_table.pk}),
            data=create_dynamic_tale_row_data,
            format="json",
        )

        # Then
        assert response.status_code == 201
        assert dynamic_table.dynamic_table_model.objects.count() == 1
        assert response.data["test_string"] == create_dynamic_tale_row_data["test_string"]
        assert response.data["test_number"] == create_dynamic_tale_row_data["test_number"]
        assert response.data["test_bool"] == create_dynamic_tale_row_data["test_bool"]

    def test_dynamic_table_respects_schema(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        dynamic_table = DynamicTable.objects.create(name="test_table", user=api_test_user)
        dynamic_fields = [
            DynamicField(name="test_string", type="STRING", dynamic_table=dynamic_table),
            DynamicField(name="test_number", type="NUMBER", dynamic_table=dynamic_table),
            DynamicField(name="test_bool", type="BOOLEAN", dynamic_table=dynamic_table),
        ]
        DynamicField.objects.bulk_create(dynamic_fields)
        dynamic_table.create_dynamic_table_in_db()

        create_dynamic_tale_row_data = {
            "test_string": "test",
            "test_number": 1,
            "bad_field": True,
        }

        # When
        response = api_client.post(
            reverse("api:dynamictable-row", kwargs={"pk": dynamic_table.pk}),
            data=create_dynamic_tale_row_data,
            format="json",
        )

        # Then
        assert response.status_code == 400
        assert dynamic_table.dynamic_table_model.objects.count() == 0

    def test_get_data_from_dynamic_table(self, db, api_client: APIClient, api_test_user: User) -> None:
        # Given
        dynamic_table = DynamicTable.objects.create(name="test_table", user=api_test_user)
        dynamic_fields = [
            DynamicField(name="test_string", type="STRING", dynamic_table=dynamic_table),
            DynamicField(name="test_number", type="NUMBER", dynamic_table=dynamic_table),
            DynamicField(name="test_bool", type="BOOLEAN", dynamic_table=dynamic_table),
        ]
        DynamicField.objects.bulk_create(dynamic_fields)
        dynamic_table.create_dynamic_table_in_db()

        dynamic_table_object_one = dynamic_table.dynamic_table_model.objects.create(
            test_string="test", test_number=1, test_bool=True
        )
        dynamic_table_object_two = dynamic_table.dynamic_table_model.objects.create(
            test_string="test_2", test_number=2, test_bool=False
        )

        # When
        response = api_client.get(reverse("api:dynamictable-rows", kwargs={"pk": dynamic_table.pk}), format="json")

        # Then
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["test_string"] == dynamic_table_object_one.test_string
        assert response.data[0]["test_number"] == dynamic_table_object_one.test_number
        assert response.data[0]["test_bool"] == dynamic_table_object_one.test_bool
        assert response.data[1]["test_string"] == dynamic_table_object_two.test_string
        assert response.data[1]["test_number"] == dynamic_table_object_two.test_number
        assert response.data[1]["test_bool"] == dynamic_table_object_two.test_bool
