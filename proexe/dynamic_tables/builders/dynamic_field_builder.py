from typing import Protocol

from django.db import models

from proexe.dynamic_tables.models import DynamicField


class FieldBuilder(Protocol):
    TYPE: str

    def build(self, dynamic_field: DynamicField) -> models.Field:
        ...


class StringFieldBuilder(FieldBuilder):
    TYPE = DynamicField.Type.STRING

    def build(self, dynamic_field: DynamicField) -> models.Field:
        return models.CharField(max_length=63)


class NumberFieldBuilder(FieldBuilder):
    TYPE = DynamicField.Type.NUMBER

    def build(self, dynamic_field: DynamicField) -> models.Field:
        return models.FloatField()


class BooleanFieldBuilder(FieldBuilder):
    TYPE = DynamicField.Type.BOOLEAN

    def build(self, dynamic_field: DynamicField) -> models.Field:
        return models.BooleanField()


class DynamicFieldsBuilder:
    _FIELD_TYPE__BUILDER: dict[str, FieldBuilder] = {
        DynamicField.Type.NUMBER: NumberFieldBuilder(),
        DynamicField.Type.STRING: StringFieldBuilder(),
        DynamicField.Type.BOOLEAN: BooleanFieldBuilder(),
    }

    def build(self, dynamic_fields: list[DynamicField]) -> dict[str, models.Field]:
        django_fields = {}

        for dynamic_field in dynamic_fields:
            field_builder = self._FIELD_TYPE__BUILDER[dynamic_field.type]
            django_field = field_builder.build(dynamic_field)
            django_fields[dynamic_field.name] = django_field

        return django_fields
