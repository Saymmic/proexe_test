import uuid

from django.db import models
from model_utils.models import TimeStampedModel


class UUIDPrimaryKeyModel(models.Model):
    """
    An abstract base class model that provides primary key id as uuid.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDPrimaryKeyModel, TimeStampedModel):
    class Meta(UUIDPrimaryKeyModel.Meta, TimeStampedModel.Meta):
        abstract = True
        get_latest_by = "created"
