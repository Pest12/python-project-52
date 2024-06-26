# Generated by Django 5.0.1 on 2024-04-05 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
        ('statuses', '0001_initial'),
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='taskTOauthor', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='taskTOdoer', to=settings.AUTH_USER_MODEL, verbose_name='Executor'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.statuses', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='tasktolabel',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='labels.labels'),
        ),
        migrations.AddField(
            model_name='tasktolabel',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.tasks'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, through='tasks.TaskToLabel', to='labels.labels'),
        ),
    ]
