# Generated by Django 4.2.3 on 2023-09-10 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0025_revision_revision_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="studytask",
            name="is_visible",
            field=models.BooleanField(default=True),
        ),
    ]
