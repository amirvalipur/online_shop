# Generated by Django 4.2.6 on 2023-11-08 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_finaly',
        ),
    ]