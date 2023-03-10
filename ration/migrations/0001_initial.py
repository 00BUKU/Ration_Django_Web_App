# Generated by Django 3.2.12 on 2023-01-12 01:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('size', models.CharField(choices=[('S', 'Teaspoon'), ('M', 'Tablespoon'), ('L', 'Cup')], default='M', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('calorie', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('carbohydrate', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('fat', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('protein', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('summary', models.TextField(max_length=500)),
                ('directions', models.TextField()),
                ('cooking_minutes', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('preparation_minutes', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('servings', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('ingredient', models.ManyToManyField(through='ration.Amount', to='ration.Ingredient')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(max_length=250)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ration.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('daily_calorie', models.FloatField(default=2000.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('daily_carbohydrate', models.FloatField(default=300.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('daily_fat', models.FloatField(default=65.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('daily_protein', models.FloatField(default=50.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('favorites', models.ManyToManyField(blank=True, to='ration.Recipe')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servings', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('meal', models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner'), ('S', 'Snack')], default='B', max_length=1)),
                ('date', models.DateField(verbose_name='Meal date')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ration.profile')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ration.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='amount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ration.ingredient'),
        ),
        migrations.AddField(
            model_name='amount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ration.recipe'),
        ),
    ]
