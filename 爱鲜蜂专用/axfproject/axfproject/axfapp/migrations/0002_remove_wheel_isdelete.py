# Generated by Django 2.2.7 on 2020-02-29 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('axfapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wheel',
            name='isDelete',
        ),
    ]
