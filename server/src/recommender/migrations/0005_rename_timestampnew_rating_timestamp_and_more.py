# Generated by Django 5.0.3 on 2024-03-22 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0004_remove_rating_timestamp_remove_tag_timestamp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='timestampNew',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='timestampNew',
            new_name='timestamp',
        ),
    ]
