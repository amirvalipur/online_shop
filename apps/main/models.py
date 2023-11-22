from django.utils import timezone
from django.db import models
from utils import FileUpload
from django.utils.safestring import mark_safe


class Slider(models.Model):
    slider_title1 = models.CharField(verbose_name="متن اول", max_length=200, null=True, blank=True)
    slider_title2 = models.CharField(verbose_name="متن دوم", max_length=200, null=True, blank=True)
    slider_title3 = models.CharField(verbose_name="متن سوم", max_length=200, null=True, blank=True)
    file_upload = FileUpload('images', 'slider')
    image_name = models.ImageField(upload_to=file_upload.upload_to, blank=True, null=True, verbose_name='تصویر اسلاید')
    slider_link = models.URLField(verbose_name="لینک اسلاید", max_length=200, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="فعال/غیرفعال", default=True, blank=True)
    register_datetime = models.DateTimeField(verbose_name='تاریخ درج', auto_now_add=True)
    publish_date = models.DateField(verbose_name='تاریخ انتشار', default=timezone.now)
    update_datetime = models.DateTimeField(verbose_name='تاریخ آخرین بروزرسانی', auto_now=True)

    def __str__(self):
        return f'{self.slider_title1}'

    class Meta:
        verbose_name = "اسلاید"
        verbose_name_plural = "اسلایدها"


    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_name}" style="width:80px;height:60px;">')

    image_slide.short_description = 'تصویر اسلاید'

    def link(self):
        return mark_safe(f'<a href="{self.slider_link}" target="_blank">link</a>')

    link.short_description = 'پیوندها'