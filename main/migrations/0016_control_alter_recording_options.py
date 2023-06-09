# Generated by Django 4.2 on 2023-04-21 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0015_recodringsession_recordings_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Control",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("int_value", models.IntegerField(blank=True, null=True)),
                ("bool_value", models.BooleanField(blank=True, null=True)),
                (
                    "string_value",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("datetime_value", models.DateTimeField(blank=True, null=True)),
                ("float_value", models.FloatField(blank=True, null=True)),
                ("json_value", models.JSONField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Control",
                "verbose_name_plural": "Controls",
                "ordering": ["name"],
            },
        ),
        migrations.AlterModelOptions(
            name="recording",
            options={"verbose_name": "Recording", "verbose_name_plural": "Recordings"},
        ),
    ]
