import json

from django.urls import reverse


class TestCreateDynamicTableView:
    def test_post_valid_request(self, db, api_client) -> None:
        # Given
        create_data = {
            "name": "test_table",
            "fields": [
                {"name": "test_string", "type": "STRING"},
                {"name": "test_number", "type": "NUMBER"},
                {"name": "test_bool", "type": "BOOLEAN"},
            ],
            "description": "test_description",
        }

        # When
        response = api_client.post(reverse("api:dynamic_tables:create_table"), create_data, format="json")

        # Then
        assert response.status_code == 201
        response.data.pop("uuid")
        assert json.dumps(response.data) == json.dumps(
            {
                "name": "test_table",
                "description": "test_description",
                "fields": [
                    {"name": "test_string", "type": "STRING"},
                    {"name": "test_number", "type": "NUMBER"},
                    {"name": "test_bool", "type": "BOOLEAN"},
                ],
            }
        )
