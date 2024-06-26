# Generated by Django 4.2.3 on 2024-03-14 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='skimpyTurtle', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_reminder',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='userID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
