# Generated by Django 4.2.3 on 2024-03-26 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_grocery_custom_reminder_grocery_day_before_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('instructions', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='security_question',
            name='question',
        ),
    ]
