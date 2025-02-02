# Generated by Django 5.0.3 on 2024-03-22 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_link_tmdbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='imdbId',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='tmdbId',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
