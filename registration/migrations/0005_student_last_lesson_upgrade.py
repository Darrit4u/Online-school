# Generated by Django 4.0.3 on 2022-04-26 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_student_upgrade'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='last_lesson_upgrade',
            field=models.IntegerField(default=0),
        ),
    ]
