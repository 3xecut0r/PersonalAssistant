# Generated by Django 4.2.4 on 2023-09-07 15:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Notes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="tags",
            field=models.ManyToManyField(blank=True, null=True, to="Notes.tag"),
        ),
    ]
