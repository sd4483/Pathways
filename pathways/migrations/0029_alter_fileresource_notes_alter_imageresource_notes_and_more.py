# Generated by Django 4.2.3 on 2023-09-11 15:20

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0028_alter_textresource_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fileresource",
            name="notes",
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name="imageresource",
            name="notes",
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name="linkresource",
            name="notes",
            field=django_quill.fields.QuillField(),
        ),
    ]
