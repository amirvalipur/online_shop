from django.db import models
from django.urls import reverse
from utils import FileUpload
from django.utils import timezone
from datetime import datetime
from jalali_date import date2jalali


class Brand(models.Model):
    brand_title = models.CharField(max_length=50, verbose_name='نام برند')
    file_upload = FileUpload('images', 'brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر')
    slug = models.SlugField(max_length=50, null=True)

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.brand_title


class ProductGroup(models.Model):
    group_title = models.CharField(max_length=50, verbose_name='نام گروه کالا')
    file_upload = FileUpload('images', 'product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر گروه کالا')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    group_parent = models.ForeignKey('ProductGroup', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='والد گروه کالا', related_name='groups')
    slug = models.SlugField(max_length=50, null=True)

    class Meta:
        verbose_name = 'گروه کالا'
        verbose_name_plural = 'گروه های کالا'

    def __str__(self):
        return self.group_title


class Feature(models.Model):
    feature_name = models.CharField(max_length=100, verbose_name='نام ویژگی')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا',
                                           related_name='features_of_product_group')
    slug = models.SlugField(max_length=100, null=True)

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'

    def __str__(self):
        return self.feature_name


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='نام کالا')
    file_upload = FileUpload('images', 'product')
    image_name = models.ImageField(upload_to=file_upload.upload_to, blank=True, null=True, verbose_name='تصویر کالا')
    summery_description = models.TextField(default=None, null=True, blank=True, verbose_name='خلاصه توضیحات')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='products_of_group')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, verbose_name='برند کالا',
                              related_name='products_of_brand')
    feature = models.ManyToManyField(Feature, through='ProductFeature')
    slug = models.SlugField(max_length=100, null=True)
    register_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ بروز رسانی')
    publish_date = models.DateField(default=timezone.now, verbose_name='تاریخ انتشار')

    # ________________________________________________________
    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    # ________________________________________________________
    def get_price_by_discount(self):
        list1 = []
        for dis_bas_detail in self.discount_basket_details2.all():
            if (
                    dis_bas_detail.discount_basket.is_active == True and
                    dis_bas_detail.discount_basket.start_date <= datetime.now() and
                    dis_bas_detail.discount_basket.end_date >= datetime.now()
            ):
                list1.append(dis_bas_detail.discount_basket.discount)
        discount = 0
        if len(list1) > 0:
            discount = max(list1)
        return int(self.price - (self.price * discount / 100))

    # ________________________________________________________

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا ها'

    def __str__(self):
        return self.product_name

    def convert_date_time(self):
        jalali_date = date2jalali(self.publish_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time.short_description = 'تاریخ انتشار'

# ____________________________________________________________________
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=50, verbose_name='مقدار ویژگی')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ویژگی',
                                related_name='feature_values')

    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی'

    def __str__(self):
        return self.value_title


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا',
                                related_name='product_of_features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name='ویژگی', related_name='features')
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name='مقدار ویژگی')
    filter_value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='فیلتر مقدار',
                                     related_name='product_feature')

    class Meta:
        verbose_name = 'ویژگی کالا'
        verbose_name_plural = 'ویژگی های کالا'

    def __str__(self):
        return f'{self.feature} {self.product} : {self.value}'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا',
                                related_name='gallery_of_product')
    file_upload = FileUpload('images', 'product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر کالا'
        verbose_name_plural = 'تصاویر کالا'
