from django.contrib import admin
from .models import *
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(Coupon)
class CouponAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['coupon_code', 'convert_date_time_start', 'convert_date_time_end', 'discount', 'is_active']
    ordering = ['is_active']


class DiscountBasketDetailsInline(admin.TabularInline):
    model = DiscountBasketDetails
    extra = 3


@admin.register(DiscountBasket)
class DiscountBasketAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['discount_title', 'convert_date_time_start', 'convert_date_time_end', 'is_active']
    ordering = ['is_active']
    inlines = [DiscountBasketDetailsInline]

