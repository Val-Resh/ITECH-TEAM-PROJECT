# Generated by Django 2.1.5 on 2022-03-13 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20220313_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='image',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]