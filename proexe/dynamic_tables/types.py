from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, TypeVar

from django.db import models
from rest_framework import serializers

if TYPE_CHECKING:
    from proexe.dynamic_tables.models import Field

# Generic type for a Django model
# Reference: https://mypy.readthedocs.io/en/stable/kinds_of_types.html#the-type-of-class-objects
DjangoModelType = TypeVar("DjangoModelType", bound=models.Model)
DjangoModelFieldType = TypeVar("DjangoModelFieldType", bound=models.Field)
DjangoModelSerializerType = TypeVar("DjangoModelSerializerType", bound=serializers.ModelSerializer)


class FieldDataType(TypedDict):
    uuid: str | None
    name: str
    type: Field.Type
