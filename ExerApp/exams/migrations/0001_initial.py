# Generated by Django 4.1.4 on 2023-02-14 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('excercises', '0007_alter_exerciseset_categories'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('start_at', models.DateTimeField(blank=True)),
                ('end_at', models.DateTimeField(blank=True)),
                ('exercise_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='excercises.exerciseset')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExamSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('start_at', models.DateTimeField(auto_now_add=True)),
                ('end_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
            ],
        ),
        migrations.CreateModel(
            name='SessionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.CharField(max_length=255)),
                ('exam_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.examsession')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='excercises.content')),
            ],
        ),
    ]
