# Generated by Django 3.1.12 on 2022-08-15 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dividends_info', '0003_stockinfo_last_updated_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockinfo',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
