# Generated by Django 3.1.2 on 2020-10-23 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20201023_0438'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='title', max_length=111),
            preserve_default=False,
        ),
    ]
