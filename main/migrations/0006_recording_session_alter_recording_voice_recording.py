# Generated by Django 4.2 on 2023-04-12 05:28

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_recording_delete_record"),
    ]

    operations = [
        migrations.AddField(
            model_name="recording",
            name="session",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="recording",
            name="voice_recording",
            field=models.FileField(upload_to=main.models.recording_path),
        ),
    ]
