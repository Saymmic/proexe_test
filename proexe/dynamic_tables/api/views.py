from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from proexe.dynamic_tables.api.serializers import DynamicTableSerializer
from proexe.dynamic_tables.builders.dynamic_table_serializer_builder import DynamicTableSerializerBuilder
from proexe.dynamic_tables.models import DynamicTable


class DynamicTableViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = DynamicTable.objects.all()
    serializer_class = DynamicTableSerializer

    def get_queryset(self) -> QuerySet[DynamicTable]:
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer: DynamicTableSerializer) -> None:
        serializer.save(user=self.request.user)

    def perform_update(self, serializer: DynamicTableSerializer) -> None:
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def rows(self, request, pk=None):
        dynamic_table_serializer_builder = DynamicTableSerializerBuilder()
        dynamic_table = self.get_object()
        serializer_class = dynamic_table_serializer_builder.build(dynamic_table)
        queryset = dynamic_table.dynamic_table_model.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def row(self, request, pk=None):
        dynamic_table_serializer_builder = DynamicTableSerializerBuilder()
        dynamic_table = self.get_object()
        serializer_class = dynamic_table_serializer_builder.build(dynamic_table)
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
