# Generated by Django 4.2 on 2023-04-29 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_remove_tuser_subscription_tuser_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tuser",
            name="balance",
            field=models.FloatField(default=0.09),
        ),
    ]
