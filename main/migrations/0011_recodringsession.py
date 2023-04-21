# Generated by Django 4.2 on 2023-04-18 04:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0010_recording_audio_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecodringSession",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("session", models.IntegerField()),
                ("started", models.DateTimeField(auto_now_add=True)),
                ("ended", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Recording Session",
                "verbose_name_plural": "Recording Sessions",
            },
        ),
    ]