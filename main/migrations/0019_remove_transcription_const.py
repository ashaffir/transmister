# Generated by Django 4.2 on 2023-04-29 19:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0018_transcription_const"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transcription",
            name="const",
        ),
    ]