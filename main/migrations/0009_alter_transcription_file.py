# Generated by Django 4.2 on 2023-04-13 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_transcription_file_transcription_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcription',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
