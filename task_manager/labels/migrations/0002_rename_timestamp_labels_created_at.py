# Generated by Django 5.0.1 on 2024-03-28 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labels',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]
