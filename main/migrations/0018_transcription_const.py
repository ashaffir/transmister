# Generated by Django 4.2 on 2023-04-29 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0017_transcription_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="transcription",
            name="const",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
