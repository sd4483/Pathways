# Generated by Django 4.2.3 on 2023-09-09 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0019_remove_fileresource_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileresource",
            name="name",
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]