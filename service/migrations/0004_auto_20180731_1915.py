# Generated by Django 2.0.4 on 2018-07-31 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20180730_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 31, 19, 15, 57, 909675)),
        ),
    ]
