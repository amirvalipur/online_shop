from django.db import models
from apps.accounts.models import CustomUser
from utils import FileUpload
from django.utils import timezone
from jalali_date import date2jalali


class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'

    def __str__(self):
        return f'{self.user}'


class Blog(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='نویسنده', related_name='blogs')
    blog_title = models.CharField(max_length=100, verbose_name='عنوان مقاله')
    blog_text = models.TextField(verbose_name='متن مقاله')
    file_upload = FileUpload('images', 'blogs')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر مقاله', blank=True, null=True)
    register_date = models.DateField(auto_now_add=True, verbose_name='تاریخ درج')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    publish_date = models.DateField(default=timezone.now, verbose_name='تاریخ انتشار')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')
    slug = models.SlugField(max_length=50, null=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return f'{self.blog_title}  {self.author}'

    def convert_date_time(self):
        jalali_date = date2jalali(self.publish_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time.short_description = 'تاریخ انتشار'
