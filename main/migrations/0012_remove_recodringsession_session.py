# Generated by Django 4.2 on 2023-04-18 04:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0011_recodringsession"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recodringsession",
            name="session",
        ),
    ]
