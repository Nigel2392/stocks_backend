# Generated by Django 4.0.6 on 2022-08-13 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dividends_info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockinfo',
            name='ticker',
            field=models.CharField(default='fake', max_length=100),
            preserve_default=False,
        ),
    ]
