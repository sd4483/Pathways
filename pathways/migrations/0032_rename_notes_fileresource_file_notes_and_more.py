# Generated by Django 4.2.3 on 2023-09-11 16:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0031_alter_linkresource_notes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="fileresource",
            old_name="notes",
            new_name="file_notes",
        ),
        migrations.RenameField(
            model_name="imageresource",
            old_name="notes",
            new_name="image_notes",
        ),
        migrations.RenameField(
            model_name="linkresource",
            old_name="notes",
            new_name="link_notes",
        ),
    ]
