# Generated by Django 4.2 on 2023-04-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_tuser_subscription"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tuser",
            name="subscription",
        ),
        migrations.AddField(
            model_name="tuser",
            name="balance",
            field=models.FloatField(default=0),
        ),
    ]
