# Generated by Django 4.2.3 on 2023-07-26 20:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dynamic_tables", "0002_field_table_remove_dynamictable_user_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="field",
            old_name="dynamic_table",
            new_name="table",
        ),
    ]