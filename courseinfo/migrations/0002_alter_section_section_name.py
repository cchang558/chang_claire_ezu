# Generated by Django 4.1.7 on 2023-02-18 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courseinfo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="section",
            name="section_name",
            field=models.CharField(max_length=20),
        ),
    ]
