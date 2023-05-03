# Generated by Django 4.2 on 2023-05-01 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0023_remove_recording_language_transcription_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="recodringsession",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="transcription",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transcriptions",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]