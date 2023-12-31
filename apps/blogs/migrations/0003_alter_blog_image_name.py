# Generated by Django 4.2.6 on 2023-11-08 10:42

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blog_slug_alter_blog_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر مقاله'),
        ),
    ]
