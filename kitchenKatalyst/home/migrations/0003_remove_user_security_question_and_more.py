# Generated by Django 4.2.3 on 2024-03-14 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_user_username_alter_user_date_reminder_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='security_question',
        ),
        migrations.RemoveField(
            model_name='user',
            name='security_question_answer',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
