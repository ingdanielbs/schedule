# Generated by Django 4.2.5 on 2023-12-19 03:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_coursestudent_course_coursestudent_dateupdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCompetence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentNumber', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('competence', models.CharField(max_length=255)),
                ('learningResult', models.CharField(max_length=255)),
                ('evaluationJudgment', models.CharField(max_length=50)),
                ('official', models.CharField(max_length=70)),
                ('dateUpdate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
    ]
