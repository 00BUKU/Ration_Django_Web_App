# Generated by Django 3.2.12 on 2023-01-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='summary',
            field=models.TextField(default='1', max_length=500),
            preserve_default=False,
        ),
    ]