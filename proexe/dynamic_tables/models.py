from __future__ import annotations

from functools import cached_property
from typing import Type

from django.db import models

from proexe.dynamic_tables.managers import DynamicFieldManager, DynamicTableManager
from proexe.dynamic_tables.querysets import DynamicFieldQuerySet, DynamicTableQuerySet
from proexe.utils.models import BaseModel


class DynamicTable(BaseModel):
    name = models.CharField(max_length=63)  # 63 is the max length of a table name in postgres
    meta = models.JSONField(null=True, blank=True, default=dict)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="dynamic_tables")

    objects = DynamicTableManager.from_queryset(DynamicTableQuerySet)()

    def __str__(self):
        return f"{self.name} - {self.user}"

    def create_dynamic_table_in_db(self) -> Type[models.Model]:
        return DynamicTable.objects.create_dynamic_table_in_db(self)

    @cached_property
    def dynamic_table_model(self) -> Type[models.Model]:
        return DynamicTable.objects.build_dynamic_table_model(self)


class DynamicField(BaseModel):
    class Type(models.TextChoices):
        NUMBER = "NUMBER"
        STRING = "STRING"
        BOOLEAN = "BOOLEAN"

    name = models.CharField(max_length=63)  # 63 is the max length of a column name in postgres
    type = models.CharField(max_length=32, choices=Type.choices)

    # Can be added parameters for fields like max_length, null, blank, etc.
    # For now, we will keep it simple

    dynamic_table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE, related_name="dynamic_fields")

    objects = DynamicFieldManager.from_queryset(DynamicFieldQuerySet)()

    def __str__(self):
        return f"{self.name}:{self.type}"
