from django.urls import path
from .views import *

app_name = 'payments'
urlpatterns = [
    # path('zarinpal_payment/<int:order_id/>', ZarinpalPaymentView.as_view(), name='zarinpal_payment'),
    # path('verify_zarinpal_payment/', ZarinpalPaymentVerifyView.as_view(), name='verify_zarinpal_payment'),
    path('all_receipts/', AllReceipts.as_view(), name='all_receipts'),
    path('user_receipt/<int:payment_id>/', UserReceipt.as_view(), name='user_receipt'),
    path('result_receipt/<int:payment_id>/', result_receipt, name='result_receipt'),
    path('verify_status/<str:message>/<int:type>/', show_verification_message, name='verify_status'),
    path('verify_zarinpal_payment/<int:order_id>/', ZarinpalPaymentVerifyView.as_view(),
         name='verify_zarinpal_payment'),
]
