# Generated by Django 4.2.3 on 2023-09-09 12:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0018_fileresource_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fileresource",
            name="name",
        ),
    ]
