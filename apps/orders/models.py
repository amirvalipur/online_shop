from django.db import models
from django.utils import timezone
from uuid import uuid4
from jalali_date import date2jalali

import utils
from apps.products.models import Product
from apps.accounts.models import Customer


class PaymentType(models.Model):
    payment_title = models.CharField(max_length=50, verbose_name='نوع پرداخت')

    def __str__(self):
        return self.payment_title

    class Meta:
        verbose_name = 'نوع پرداخت'
        verbose_name_plural = 'انواع روش پرداخت'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='مشتری')
    register_date = models.DateField(default=timezone.now, verbose_name='تاریخ درج سفارش')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ ویرایش سفارش')
    order_code = models.UUIDField(unique=True, default=uuid4, editable=False, verbose_name='کد تولیدی برای سفارش')
    is_finally = models.BooleanField(default=False, verbose_name='نهایی شده')
    discount = models.IntegerField(blank=True, null=True, default=0, verbose_name='تخفیف روی فاکتور')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    payment_type = models.ForeignKey(PaymentType, default=1, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='نوع پرداخت', related_name='payment_types')

    def get_order_total_price(self):
        total_price = 0
        for item in self.orders_details1.all():
            total_price += item.price * item.qty
        order_final_price, delivery, tax = utils.price_by_delivery_tax(total_price, self.discount)
        return int(order_final_price * 10)

    def __str__(self):
        return f'{self.id}\t{self.is_finally}'

    def convert_date_time(self):
        jalali_date = date2jalali(self.register_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time.short_description = 'تاریخ انتشار'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders_details1', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders_details2', verbose_name='کالا')
    qty = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت کالا در فاکتور')

    def __str__(self):
        return f'{self.order}\t{self.product}\t{self.qty}\t{self.price}'

    def detail_sub_total_price(self):
        return int(self.price * self.qty)
