# Generated by Django 4.2.3 on 2023-08-28 12:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0007_studytask_pathway"),
    ]

    operations = [
        migrations.AddField(
            model_name="studytask",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
