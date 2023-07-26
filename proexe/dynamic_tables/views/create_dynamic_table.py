from django.db import connections
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from proexe.dynamic_tables.adapters.django_dynamic_field_repository import DjangoDynamicFieldRepository
from proexe.dynamic_tables.adapters.django_dynamic_table_builder import DjangoDynamicTableBuilder
from proexe.dynamic_tables.adapters.django_dynamic_table_repository import DjangoDynamicTableRepository
from proexe.dynamic_tables.adapters.django_schema_editor import DjangoSchemaEditor
from proexe.dynamic_tables.domain.use_cases.create_dynamic_table import CreateDynamicTableUseCase
from proexe.dynamic_tables.models import DynamicField


class FieldInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=DynamicField.Type.choices)


class TableInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    fields = FieldInputSerializer(many=True)
    description = serializers.CharField(required=False)


class OutputSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    fields = FieldInputSerializer(many=True, source="dynamic_fields")


class CreateDynamicTableAPIView(APIView):
    def post(self, request, *args, **kwargs):
        input_serializer = TableInputSerializer(data=request.data)

        input_serializer.is_valid(raise_exception=True)

        create_dynamic_table_use_case = CreateDynamicTableUseCase(
            dynamic_table_builder=DjangoDynamicTableBuilder(),
            schema_editor=DjangoSchemaEditor(connection=connections["default"]),
            dynamic_table_repository=DjangoDynamicTableRepository(),
            dynamic_field_repository=DjangoDynamicFieldRepository(),
        )

        dynamic_table = create_dynamic_table_use_case.execute(
            name=input_serializer.validated_data["name"],
            fields=input_serializer.validated_data["fields"],
            description=input_serializer.validated_data.get("description"),
            user=request.user,
        )
        # TODO: Add uuid
        output_serializer = OutputSerializer(instance=dynamic_table)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
