from typing import Protocol, Type

from django.db import models

from proexe.dynamic_tables.domain.ports.dynamic_table_builder import DynamicTableBuilder
from proexe.dynamic_tables.types import DynamicFieldProtocol, DynamicTableProtocol


class FieldBuilder(Protocol):
    TYPE: str

    def build(self, dynamic_field: DynamicFieldProtocol) -> models.Field:
        ...


class StringFieldBuilder(FieldBuilder):
    TYPE = DynamicFieldProtocol.Type.STRING

    def build(self, dynamic_field: DynamicFieldProtocol) -> models.Field:
        return models.CharField(max_length=63)


class NumberFieldBuilder(FieldBuilder):
    TYPE = DynamicFieldProtocol.Type.NUMBER

    def build(self, dynamic_field: DynamicFieldProtocol) -> models.Field:
        return models.FloatField()


class BooleanFieldBuilder(FieldBuilder):
    TYPE = DynamicFieldProtocol.Type.BOOLEAN

    def build(self, dynamic_field: DynamicFieldProtocol) -> models.Field:
        return models.BooleanField()


class DjangoDynamicTableBuilder(DynamicTableBuilder):
    """
    Builder design pattern
    """

    _FIELD_TYPE__BUILDER: dict[str, FieldBuilder] = {
        DynamicFieldProtocol.Type.NUMBER: NumberFieldBuilder(),
        DynamicFieldProtocol.Type.STRING: StringFieldBuilder(),
        DynamicFieldProtocol.Type.BOOLEAN: BooleanFieldBuilder(),
    }

    def _build_name(self, dynamic_table: DynamicTableProtocol) -> str:
        table_name = f"{dynamic_table.user.username}_{dynamic_table.name}"

        return table_name

    def _build_fields(self, dynamic_table: DynamicTableProtocol) -> dict[str, models.Field]:
        django_fields = {}

        for dynamic_field in dynamic_table.dynamic_fields:
            field_builder = self._FIELD_TYPE__BUILDER[dynamic_field.type]
            django_field = field_builder.build(dynamic_field)
            django_fields[dynamic_field.name] = django_field

        return django_fields

    # We can add other steps to build model
    # def _build_meta(self) -> Type:
    #     class Meta:
    #         pass
    #
    #     return Meta

    def _build_app_label(self, dynamic_table: DynamicTableProtocol) -> str:
        pass

    def build(self, dynamic_table: DynamicTableProtocol) -> models.Model:
        name = self._build_name(dynamic_table)
        fields = self._build_fields(dynamic_table)
        # meta = self._build_meta()

        model: models.Model = type(name, (models.Model,), {"__module__": "proexe.dynamic_tables.models", **fields})

        return model
