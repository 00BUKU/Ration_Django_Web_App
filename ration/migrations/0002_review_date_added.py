# Generated by Django 4.1.4 on 2023-01-06 17:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
