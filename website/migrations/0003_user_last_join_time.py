# Generated by Django 2.1.5 on 2022-03-11 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20220311_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_join_time',
            field=models.DateTimeField(null=True),
        ),
    ]