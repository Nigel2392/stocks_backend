# Generated by Django 3.1.12 on 2022-08-20 18:59

import dividends_info.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dividends_info', '0004_auto_20220815_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockinfo',
            name='earnings',
            field=djongo.models.fields.ArrayField(model_container=dividends_info.models.Earning, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='dividends',
            field=djongo.models.fields.ArrayField(model_container=dividends_info.models.Dividend, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='sector',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stockinfo',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
