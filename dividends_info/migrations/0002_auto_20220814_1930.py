# Generated by Django 3.1.12 on 2022-08-14 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dividends_info', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockinfo',
            old_name='description',
            new_name='summary',
        ),
    ]
