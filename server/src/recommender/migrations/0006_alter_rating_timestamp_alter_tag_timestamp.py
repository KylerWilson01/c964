# Generated by Django 5.0.3 on 2024-03-22 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0005_rename_timestampnew_rating_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='timestamp',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='tag',
            name='timestamp',
            field=models.BigIntegerField(),
        ),
    ]
