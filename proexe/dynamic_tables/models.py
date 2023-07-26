from __future__ import annotations

from functools import cached_property
from typing import Type

from django.db import models

from proexe.utils.models import BaseModel


class Table(BaseModel):
    name = models.CharField(max_length=63)  # 63 is the max length of a table name in postgres
    meta = models.JSONField(null=True, blank=True, default=dict)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="tables")

    def __str__(self):
        return f"{self.name} - {self.user}"


class Field(BaseModel):
    class Type(models.TextChoices):
        NUMBER = "NUMBER"
        STRING = "STRING"
        BOOLEAN = "BOOLEAN"

    name = models.CharField(max_length=63)  # 63 is the max length of a column name in postgres
    type = models.CharField(max_length=32, choices=Type.choices)

    # Can be added parameters for fields like max_length, null, blank, etc.
    # For now, we will keep it simple

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="fields")

    def __str__(self):
        return f"{self.name}:{self.type}"
