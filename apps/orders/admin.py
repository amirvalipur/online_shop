from django.contrib import admin
from .models import Order, OrderDetails, PaymentType


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'convert_date_time', 'is_finally', 'discount', 'payment_type']
    list_filter = ['register_date']
    inlines = [OrderDetailsInline]


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['payment_title', 'id']
