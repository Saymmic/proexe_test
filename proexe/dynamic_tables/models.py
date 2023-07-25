from __future__ import annotations

from django.db import models

from proexe.utils.models import BaseModel


class DynamicTable(BaseModel):
    name = models.CharField(max_length=63)  # 63 is the max length of a table name in postgres
    description = models.TextField(null=True, blank=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="_dynamic_tables")

    # Here we can add more META fields like  indexes, etc.
    # For now, we will keep it simple

    def __str__(self):
        return self.name

    @property
    def dynamic_fields(self) -> list[DynamicField]:
        return self._dynamic_fields.all()


class DynamicField(BaseModel):
    class Type(models.TextChoices):
        NUMBER = "NUMBER"
        STRING = "STRING"
        BOOLEAN = "BOOLEAN"

    name = models.CharField(max_length=63)  # 63 is the max length of a column name in postgres
    type = models.CharField(max_length=32, choices=Type.choices)

    # Can be added parameters for fields like max_length, null, blank, etc.
    # For now, we will keep it simple
    # The way I would do it is by inheritance or by using a JSONField not sure, need to research.

    dynamic_table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE, related_name="_dynamic_fields")

    def __str__(self):
        return f"{self.name}:{self.type}"


class DynamicTableProtocol:
    pass
