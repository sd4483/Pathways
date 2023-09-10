# Generated by Django 4.2.3 on 2023-09-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "pathways",
            "0024_remove_revision_revision_type_remove_revision_status_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="revision",
            name="revision_type",
            field=models.CharField(
                choices=[
                    ("first", "First Revision"),
                    ("second", "Second Revision"),
                    ("third", "Third Revision"),
                    ("fourth", "Fourth Revision"),
                ],
                default="FIRST",
                max_length=10,
            ),
            preserve_default=False,
        ),
    ]