from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product
from jalali_date import datetime2jalali


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, unique=True, verbose_name='کد کوپن')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = 'کوپن ها'

    def __str__(self):
        return self.coupon_code

    def convert_date_time_start(self):
        jalali_date = datetime2jalali(self.start_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time_start.short_description = 'تاریخ شروع'

    def convert_date_time_end(self):
        jalali_date = datetime2jalali(self.end_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time_end.short_description = 'تاریخ پایان'


# ______________________________________________________

class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100, verbose_name='عنوان سبد خرید')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'سبد تخفیف'
        verbose_name_plural = 'سبد های تخفیف'

    def __str__(self):
        return self.discount_title

    def convert_date_time_start(self):
        jalali_date = datetime2jalali(self.start_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time_start.short_description = 'تاریخ شروع'

    def convert_date_time_end(self):
        jalali_date = datetime2jalali(self.end_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time_end.short_description = 'تاریخ پایان'


# __________________________________________________________

class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket, on_delete=models.CASCADE, verbose_name='سبد تخفیف',
                                        related_name='discount_basket_details1')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا',
                                related_name='discount_basket_details2')

    class Meta:
        verbose_name = 'جزییات سبد تخفیف'
