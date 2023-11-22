# Generated by Django 4.2.6 on 2023-11-08 10:57

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_customer_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر پروفایل'),
        ),
    ]