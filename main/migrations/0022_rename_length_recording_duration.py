# Generated by Django 4.2 on 2023-04-30 18:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0021_recording_length_alter_recording_voice_recording"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recording",
            old_name="length",
            new_name="duration",
        ),
    ]
