# Generated by Django 4.2.6 on 2023-10-29 16:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_title', models.CharField(max_length=50, verbose_name='نام برند')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر')),
                ('slug', models.SlugField(null=True)),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=100, verbose_name='نام ویژگی')),
                ('slug', models.SlugField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'ویژگی',
                'verbose_name_plural': 'ویژگی ها',
            },
        ),
        migrations.CreateModel(
            name='FeatureValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_title', models.CharField(max_length=50, verbose_name='مقدار ویژگی')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_values', to='products.feature', verbose_name='ویژگی')),
            ],
            options={
                'verbose_name': 'مقدار ویژگی',
                'verbose_name_plural': 'مقادیر ویژگی',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, verbose_name='نام کالا')),
                ('image_name', models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا')),
                ('summery_description', models.TextField(blank=True, default=None, null=True, verbose_name='خلاصه توضیحات')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='قیمت')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('register_date', models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_date', models.DateField(auto_now=True, verbose_name='تاریخ بروز رسانی')),
                ('publish_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products_of_brand', to='products.brand', verbose_name='برند کالا')),
            ],
            options={
                'verbose_name': 'کالا',
                'verbose_name_plural': 'کالا ها',
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_title', models.CharField(max_length=50, verbose_name='نام گروه کالا')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیر فعال')),
                ('slug', models.SlugField(null=True)),
                ('group_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='products.productgroup', verbose_name='والد گروه کالا')),
            ],
            options={
                'verbose_name': 'گروه کالا',
                'verbose_name_plural': 'گروه های کالا',
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_of_product', to='products.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'تصویر کالا',
                'verbose_name_plural': 'تصاویر کالا',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=100, null=True, verbose_name='مقدار ویژگی')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='products.feature', verbose_name='ویژگی')),
                ('filter_value', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_feature', to='products.featurevalue', verbose_name='فیلتر مقدار')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_of_features', to='products.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'ویژگی کالا',
                'verbose_name_plural': 'ویژگی های کالا',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='feature',
            field=models.ManyToManyField(through='products.ProductFeature', to='products.feature'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_group',
            field=models.ManyToManyField(related_name='products_of_group', to='products.productgroup', verbose_name='گروه کالا'),
        ),
        migrations.AddField(
            model_name='feature',
            name='product_group',
            field=models.ManyToManyField(related_name='features_of_product_group', to='products.productgroup', verbose_name='گروه کالا'),
        ),
    ]