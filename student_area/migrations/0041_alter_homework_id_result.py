# Generated by Django 4.0.3 on 2022-04-30 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_area', '0040_alter_homework_id_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='id_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_area.result'),
        ),
    ]
