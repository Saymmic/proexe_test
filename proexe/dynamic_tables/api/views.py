from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from proexe.api.utils import inline_model_serializer
from proexe.dynamic_tables.models import Field, Table
from proexe.dynamic_tables.services import TableService


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

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table_service = TableService()

        table = table_service.create(
            name=serializer.validated_data["name"], fields=serializer.validated_data["fields"], user=request.user
        )

        serializer = self.OutputSerializer(table)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
