# Generated by Django 4.2.3 on 2023-09-12 03:07

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0032_rename_notes_fileresource_file_notes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fileresource",
            name="file_notes",
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="imageresource",
            name="image_notes",
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="linkresource",
            name="link_notes",
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
    ]
