# Generated by Django 4.2.6 on 2024-01-09 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nick', '0005_title_character_alter_title_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='media_type',
            field=models.CharField(blank=True, choices=[('MV', 'Movie'), ('TV', 'TV')], max_length=2),
        ),
    ]
