# Generated by Django 5.1.3 on 2024-11-18 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nippo', '0005_nippomodel_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='nippomodel',
            name='slug',
            field=models.SlugField(blank=True, max_length=20, null=True),
        ),
    ]
