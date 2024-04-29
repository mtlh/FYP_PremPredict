# Generated by Django 4.2.5 on 2024-01-20 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prempredict', '0007_remove_leaderboard_leaderboard_check_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithmprediction',
            name='correct_accuracy',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='algorithmprediction',
            name='result_accuracy',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprediction',
            name='correct_accuracy',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprediction',
            name='result_accuracy',
            field=models.PositiveIntegerField(default=0),
        ),
    ]