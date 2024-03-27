# Generated by Django 4.2.3 on 2024-03-26 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_recipe_instructions'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='home.user'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='instructions',
            field=models.TextField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
