# Generated by Django 4.2.6 on 2023-11-08 21:53

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_slider_publish_datetime_slider_publish_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر اسلاید'),
        ),
    ]
