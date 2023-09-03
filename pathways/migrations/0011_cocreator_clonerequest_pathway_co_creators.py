# Generated by Django 4.2.3 on 2023-09-03 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pathways", "0010_revision_pathway"),
    ]

    operations = [
        migrations.CreateModel(
            name="CoCreator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "pathway",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="co_creator_entries",
                        to="pathways.pathway",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="co_creator_entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CloneRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("declined", "Declined"),
                        ],
                        default="pending",
                        max_length=8,
                    ),
                ),
                (
                    "pathway",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clone_requests",
                        to="pathways.pathway",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clone_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="pathway",
            name="co_creators",
            field=models.ManyToManyField(
                blank=True,
                related_name="co_created_pathways",
                through="pathways.CoCreator",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]