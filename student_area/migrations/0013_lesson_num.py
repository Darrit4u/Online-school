# Generated by Django 4.0.3 on 2022-04-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_area', '0012_alter_question_what_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='num',
            field=models.IntegerField(default=0),
        ),
    ]
