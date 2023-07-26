from __future__ import annotations

from typing import TYPE_CHECKING, Type

from rest_framework import serializers

if TYPE_CHECKING:
    from proexe.dynamic_tables.models import DynamicTable


class DynamicTableSerializerBuilder:
    def build(self, dynamic_table: DynamicTable) -> Type[serializers.ModelSerializer]:
        class DynamicTableSerializer(serializers.ModelSerializer):
            class Meta:
                model = dynamic_table.dynamic_table_model
                fields = "__all__"

        return DynamicTableSerializer
