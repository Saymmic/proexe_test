from rest_framework import serializers

from proexe.dynamic_tables.models import DynamicField, DynamicTable


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = [
            "name",
            "type",
        ]


class DynamicTableSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=38)  # With additional user and app namespace max name will be
    fields = DynamicFieldSerializer(many=True, source="dynamic_fields")

    class Meta:
        model = DynamicTable
        fields = [
            "uuid",
            "name",
            "fields"
            # "meta", # For future development
        ]

    def create(self, validated_data: dict) -> DynamicTable:
        fields_data = validated_data.pop("dynamic_fields")
        dynamic_table = DynamicTable.objects.create(**validated_data)

        dynamic_fields = [DynamicField(dynamic_table=dynamic_table, **field_data) for field_data in fields_data]
        DynamicField.objects.bulk_create(dynamic_fields)

        dynamic_table.create_dynamic_table_in_db()

        return dynamic_table

    def update(self, instance: DynamicTable, validated_data: dict) -> DynamicTable:
        fields_data = validated_data.pop("dynamic_fields")
        updated_dynamic_table = DynamicTable.objects.create(**validated_data)

        dynamic_fields = [
            DynamicField(dynamic_table=updated_dynamic_table, **field_data) for field_data in fields_data
        ]
        DynamicField.objects.bulk_create(dynamic_fields)

        DynamicTable.objects.update_dynamic_table_in_db(
            dynamic_table=instance, new_dynamic_table=updated_dynamic_table
        )

        instance.delete()

        return updated_dynamic_table
