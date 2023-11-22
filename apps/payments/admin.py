from django.contrib import admin
from .models import Payment
from django.db.models import Q


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'amount', 'convert_date_time', 'is_finally', 'is_done')
    list_filter = ['is_done']
    list_editable = ['is_done', 'is_finally']
