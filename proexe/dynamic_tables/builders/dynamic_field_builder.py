from dataclasses import dataclass
from typing import Protocol

from django.db import models

from proexe.dynamic_tables.models import Field
from proexe.dynamic_tables.types import DjangoModelFieldType


@dataclass
class FieldDTO:
    name: str
    type: str


class FieldBuilder(Protocol):
    TYPE: str

    def build(self, field: FieldDTO) -> DjangoModelFieldType:
        ...


class StringFieldBuilder(FieldBuilder):
    TYPE = Field.Type.STRING

    def build(self, field: FieldDTO) -> DjangoModelFieldType:
        return models.CharField(max_length=63)


class NumberFieldBuilder(FieldBuilder):
    TYPE = Field.Type.NUMBER

    def build(self, field: FieldDTO) -> DjangoModelFieldType:
        return models.FloatField()


class BooleanFieldBuilder(FieldBuilder):
    TYPE = Field.Type.BOOLEAN

    def build(self, field: FieldDTO) -> DjangoModelFieldType:
        return models.BooleanField()


class DynamicFieldsBuilder:
    _FIELD_TYPE__BUILDER: dict[str, FieldBuilder] = {
        Field.Type.NUMBER: NumberFieldBuilder(),
        Field.Type.STRING: StringFieldBuilder(),
        Field.Type.BOOLEAN: BooleanFieldBuilder(),
    }

    def build(self, fields: list[FieldDTO]) -> dict[str, DjangoModelFieldType]:
        django_fields = {}

        for field in fields:
            field_builder = self._FIELD_TYPE__BUILDER[field.type]
            django_field = field_builder.build(field)
            django_fields[field.name] = django_field

        return django_fields
