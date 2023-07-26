from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from proexe.dynamic_tables.models import Table


@receiver(post_save, sender=Table)
def create_dynamic_table_in_db_signal(sender: Any, instance: Table, created: bool, **kwargs) -> None:
    if created:
        instance.create_dynamic_table_in_db()
