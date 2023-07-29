from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from proexe.api.pagination import LimitOffsetPagination, get_paginated_response
from proexe.api.utils import inline_model_serializer
from proexe.dynamic_tables.builders import DynamicFieldsBuilder, DynamicTableModelBuilder
from proexe.dynamic_tables.builders.dynamic_table_serializer_builder import DynamicTableSerializerBuilder
from proexe.dynamic_tables.models import Field, Table
from proexe.dynamic_tables.services import DynamicTableService, TableService


class TableCreateApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=38)  # With additional user and app namespace max name will be
        fields = inline_model_serializer(model=Field, model_fields=["name", "type"], many=True)

        class Meta:
            model = Table
            fields = [
                "uuid",
                "name",
                "fields"
                # "meta", # For future development
            ]

    OutputSerializer = InputSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table_service = TableService(
            dynamic_table_service=DynamicTableService(
                dynamic_table_model_builder=DynamicTableModelBuilder(
                    field_builder=DynamicFieldsBuilder(),
                ),
                dynamic_table_serializer_builder=DynamicTableSerializerBuilder(),
                dynamic_field_builder=DynamicFieldsBuilder(),
            )
        )

        table = table_service.create(
            name=serializer.validated_data["name"], fields=serializer.validated_data["fields"], user=request.user
        )

        serializer = self.OutputSerializer(table)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TableUpdateApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=38)  # With additional user and app namespace max name will be
        fields = inline_model_serializer(
            fields={"uuid": serializers.UUIDField(read_only=False, required=False)},
            model=Field,
            model_fields=["uuid", "name", "type"],
            many=True,
        )

        class Meta:
            model = Table
            fields = [
                "uuid",
                "name",
                "fields"
                # "meta", # For future development
            ]

    OutputSerializer = InputSerializer

    def put(self, request: Request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table_service = TableService(
            dynamic_table_service=DynamicTableService(
                dynamic_table_model_builder=DynamicTableModelBuilder(
                    field_builder=DynamicFieldsBuilder(),
                ),
                dynamic_table_serializer_builder=DynamicTableSerializerBuilder(),
                dynamic_field_builder=DynamicFieldsBuilder(),
            )
        )

        table = get_object_or_404(Table.objects.filter(user=request.user))

        table = table_service.update(
            table=table,
            name=serializer.validated_data["name"],
            fields=serializer.validated_data["fields"],
            user=request.user,
        )

        serializer = self.OutputSerializer(table)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DynamicTableRowCreateApi(APIView):
    def post(self, request: Request, pk: str, *args, **kwargs):
        queryset = Table.objects.filter(user=request.user)
        table = get_object_or_404(queryset=queryset, pk=pk)

        dynamic_table_service = DynamicTableService(
            dynamic_table_model_builder=DynamicTableModelBuilder(
                field_builder=DynamicFieldsBuilder(),
            ),
            dynamic_table_serializer_builder=DynamicTableSerializerBuilder(),
            dynamic_field_builder=DynamicFieldsBuilder(),
        )

        dynamic_table_serializer_class = dynamic_table_service.get_serializer_class(table=table)

        input_serializer = dynamic_table_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        dynamic_table_instance = dynamic_table_service.create_row(table=table, data=input_serializer.validated_data)

        output_serializer = dynamic_table_serializer_class(instance=dynamic_table_instance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class DynamicTableListRowsCreateApi(APIView):
    def get(self, request: Request, pk: str, *args, **kwargs):
        queryset = Table.objects.filter(user=request.user)
        table = get_object_or_404(queryset=queryset, pk=pk)

        dynamic_table_service = DynamicTableService(
            dynamic_table_model_builder=DynamicTableModelBuilder(
                field_builder=DynamicFieldsBuilder(),
            ),
            dynamic_table_serializer_builder=DynamicTableSerializerBuilder(),
            dynamic_field_builder=DynamicFieldsBuilder(),
        )
        dynamic_table_serializer_class = dynamic_table_service.get_serializer_class(table=table)

        dynamic_table_instances = dynamic_table_service.query_all(table=table)

        get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=dynamic_table_serializer_class,
            queryset=dynamic_table_instances,
            request=request,
            view=self,
        )

        output_serializer = dynamic_table_serializer_class(dynamic_table_instances, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
