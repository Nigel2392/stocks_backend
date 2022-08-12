# Generated by Django 4.0.6 on 2022-08-12 20:43

from django.db import migrations, models
import djongo.models.fields
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('searches', djongo.models.fields.ArrayField(model_container=users.models.RecentSearch)),
            ],
        ),
    ]
