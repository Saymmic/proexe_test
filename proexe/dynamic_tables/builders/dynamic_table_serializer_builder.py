from __future__ import annotations

from rest_framework import serializers

from proexe.dynamic_tables.types import DjangoModelSerializerType, DjangoModelType


class DynamicTableSerializerBuilder:
    def build(self, dynamic_table_model: DjangoModelType) -> type[DjangoModelSerializerType]:
        class DynamicTableSerializer(serializers.ModelSerializer):
            class Meta:
                model = dynamic_table_model
                fields = "__all__"

        return DynamicTableSerializer
