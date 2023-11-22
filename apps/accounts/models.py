from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from utils import FileUpload
from jalali_date import date2jalali


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, email='', name='', family='', gender=None, active_code=None, password=None):
        if not mobile_number:
            raise ValueError('شماره تلفن همراه باید وارد شود')
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            gender=gender,
            active_code=active_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, email, name, family, gender=None, active_code=None, password=None):
        user = self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            gender=gender,
            active_code=active_code,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=11, unique=True, verbose_name='شماره همراه')
    email = models.EmailField(max_length=200, blank=True, verbose_name='ایمیل')
    name = models.CharField(max_length=50, blank=True, verbose_name='نام')
    family = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی')
    GENDER_CHOICES = [('True', 'مرد'), ('False', 'زن')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, default=True,
                              verbose_name='جنسیت')
    register_date = models.DateField(default=timezone.now, verbose_name='تاریخ ثبت نام')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    active_code = models.CharField(max_length=100, null=True, blank=True, verbose_name='کد فعال سازی')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    complete_register = models.BooleanField(default=False, verbose_name='تکمیل ثبت نام', blank=True, null=True)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['email', 'name', 'family']

    objects = CustomUserManager()

    def __str__(self):
        return self.name + ' ' + self.family

    @property
    def is_staff(self):
        return self.is_admin

    def convert_date_time(self):
        jalali_date = date2jalali(self.register_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time.short_description = 'تاریخ ثبت نام'


# _________________________________________________ customer

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    landline_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='تلفن ثابت')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    file_upload = FileUpload('images', 'customer')
    image_name = models.ImageField(upload_to=file_upload.upload_to, null=True, blank=True, verbose_name='تصویر پروفایل')

    def __str__(self):
        return f'{self.user}'
