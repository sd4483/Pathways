# Generated by Django 4.2.3 on 2023-09-09 16:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0021_fileresource_cloudinary_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fileresource",
            name="cloudinary_url",
        ),
    ]