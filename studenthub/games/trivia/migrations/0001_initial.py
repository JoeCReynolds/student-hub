# Generated by Django 2.2.3 on 2019-07-22 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category', models.CharField(max_length=140, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('difficulty', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=280, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoice',
            fields=[
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='trivia.Question')),
                ('correct_answer', models.CharField(max_length=140)),
                ('incorrect_b', models.CharField(max_length=140)),
                ('incorrect_c', models.CharField(max_length=140)),
                ('incorrect_d', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='TrueFalse',
            fields=[
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='trivia.Question')),
                ('correct_answer', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField(auto_now_add=True)),
                ('datetime_end', models.DateTimeField(blank=True, null=True)),
                ('questions_correct', models.IntegerField(blank=True, null=True)),
                ('total_questions', models.IntegerField(blank=True, null=True)),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.Difficulty')),
            ],
        ),
    ]
