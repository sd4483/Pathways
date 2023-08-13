# Generated by Django 4.2.3 on 2023-08-12 15:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0002_fileresource_created_at_imageresource_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pathway",
            name="visibility",
            field=models.CharField(
                choices=[("public", "Public"), ("private", "Private")],
                default="public",
                max_length=7,
            ),
        ),
    ]
