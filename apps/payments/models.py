from django.db import models
from apps.orders.models import Order
from apps.accounts.models import Customer
from django.utils import timezone
from jalali_date import datetime2jalali


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_payments', verbose_name='سفارش')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_payments',
                                 verbose_name='مشتری')
    register_datetime = models.DateTimeField(verbose_name='تاریخ پرداخت', default=timezone.now)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی پرداخت', auto_now=True)
    amount = models.PositiveIntegerField(verbose_name='مبلغ پرداخت')
    description = models.TextField(verbose_name='توضیحات پرداخت')
    is_finally = models.BooleanField(verbose_name='وضعیت نهایی/غیرنهایی', default=False)
    is_done = models.BooleanField(verbose_name='انجام شده', default=False)
    status_code = models.IntegerField(verbose_name='کد وضعیت درگاه', blank=True, null=True)
    ref_id = models.CharField(verbose_name='شماره پیگیری پرداخت', max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.customer}'

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ‌ها'

    def convert_date_time(self):
        jalali_date = datetime2jalali(self.register_datetime).strftime('( %H:%M ) %Y/%m/%d')
        return jalali_date

    convert_date_time.short_description = 'تاریخ پرداخت'
