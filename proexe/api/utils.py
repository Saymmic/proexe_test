from typing import Any, Type

from django.db import models
from rest_framework import serializers


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = type("inline_serializer", (serializers.Serializer,), fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def inline_model_serializer(
    *,
    model: Type[models.Model],
    model_fields: list[str],
    fields: dict[str, Any] | None = None,
    data: dict | None = None,
    **kwargs,
):
    model_ = model

    class Meta:
        model = model_
        fields = model_fields

    serializer_attrs = {
        "Meta": Meta,
    }

    if fields is not None:
        serializer_attrs.update(fields)

    serializer_class = type("inline_serializer", (serializers.ModelSerializer,), serializer_attrs)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
