# Generated by Django 4.2.3 on 2023-09-03 13:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pathways", "0011_cocreator_clonerequest_pathway_co_creators"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cocreator",
            name="pathway",
        ),
        migrations.RemoveField(
            model_name="cocreator",
            name="user",
        ),
        migrations.RemoveField(
            model_name="pathway",
            name="co_creators",
        ),
        migrations.DeleteModel(
            name="CloneRequest",
        ),
        migrations.DeleteModel(
            name="CoCreator",
        ),
    ]
