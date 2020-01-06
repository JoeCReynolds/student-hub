# Generated by Django 2.2.3 on 2019-10-16 03:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flashcard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1024, unique=True)),
                ('answer', models.CharField(max_length=64)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcard.Course')),
            ],
        ),
        migrations.CreateModel(
            name='FlashcardTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=64)),
                ('flashcard', models.ManyToManyField(to='flashcard.Flashcard')),
            ],
        ),
        migrations.CreateModel(
            name='FlashcardStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.PositiveSmallIntegerField(default=0)),
                ('attempted', models.PositiveSmallIntegerField(default=0)),
                ('elapsed', models.DurationField(default=datetime.timedelta(0))),
                ('last_attempt', models.DateTimeField(default=django.utils.timezone.now)),
                ('flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcard.Flashcard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='flashcard',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcard.Module'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcard.Subject'),
        ),
    ]