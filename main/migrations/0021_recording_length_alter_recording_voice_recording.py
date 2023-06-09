# Generated by Django 4.2 on 2023-04-30 18:37

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0020_recording_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="recording",
            name="length",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="recording",
            name="voice_recording",
            field=models.FileField(
                max_length=300, upload_to=main.models.recording_path
            ),
        ),
    ]
