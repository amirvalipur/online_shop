from django.shortcuts import render, redirect
from django.views import View


import utils
from .models import Payment
from apps.accounts.models import Customer
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


# from django.conf import settings
# import requests
# import json
#
# ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"
#
#
# class ZarinpalPaymentView(LoginRequiredMixin, View):
#     def get(self, request, order_id):
#         try:
#             order = Order.objects.get(id=order_id)
#             amount = order.get_order_total_price()
#             description = 'پرداخت از طریق درگاه زرین‌پال انجام شد'
#             payment = Payment.objects.create(
#                 order=order,
#                 customer=Customer.objects.get(user=request.user),
#                 amount=amount,
#                 description=description
#             )
#             request.session['payment_session'] = {
#                 'order_id': order_id,
#                 'payment_id': payment.id
#             }
#             CallbackURL = 'http://127.0.0.1:8000/payments/verify_zarinpal_payment/'
#             phone = request.user.mobile_number
#             Email = request.user.email
#             data = {
#                 "MerchantID": settings.MERCHANT,
#                 "Amount": amount,
#                 "Description": description,
#                 "Phone": phone,
#                 "Email": Email,
#                 "CallbackURL": CallbackURL,
#             }
#             data = json.dumps(data)
#             headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#             response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#             if response.status_code == 200:
#                 response = response.json()
#                 if response['Status'] == 100:
#                     url = f"{ZP_API_STARTPAY}{response['Authority']}"
#                     return redirect(url)
#                 else:
#                     payment.status_code = response['Status']
#                     payment.save()
#                     context = {
#                         'message': f'خطا در انتقال به درگاه، کد خطا {response["Status"]}',
#                         'type': 2,
#                     }
#                     return redirect('payments:show_verification_message', context)
#             return redirect('payments:show_verification_message', f'خطا در درخواست، کد خطا {response.status_code}')
#
#         except Order.DoesNotExist:
#             return redirect('orders:checkout', order_id)
#         except Customer.DoesNotExist:
#             return redirect('orders:checkout', order_id)
#         except requests.exceptions.Timeout as e:
#             context = {
#                 'message': f'خطا {e}',
#                 'type': 2,
#             }
#             return redirect('payments:show_verification_message', context)
#         except requests.exceptions.ConnectionError as e:
#             context = {
#                 'message': f'خطا {e}',
#                 'type': 2,
#             }
#             return redirect('payments:show_verification_message', context)
#
# # ____________________________________________________________________________________
#
#
# class ZarinpalPaymentVerifyView(LoginRequiredMixin, View):
#     def get(self, request):
#         t_status = request.GET.get('Status')
#         t_authority = request.GET.get('Authority')
#         if request.GET.get('Status') == 'OK':
#             order_id = request.session['payment_session']['order_id']
#             payment_id = request.session['payment_session']['payment_id']
#             order = Order.objects.get(id=order_id)
#             payment = Payment.objects.get(id=payment_id)
#
#             req_header = {'accept': 'application/json', 'content-type': 'application/json'}
#             req_data = {
#                 'merchant_id': '',
#                 'amount': order.get_order_total_price(),
#                 'authority': t_authority,
#             }
#
#             req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
#
#             if len(req.json()['errors']) == 0:
#                 t_status = req.json()['data']['code']
#                 if t_status == 100:
#                     order.is_finally = True
#                     order.save()
#
#                     payment.is_finally = True
#                     payment.status_code = t_status
#                     payment.ref_id = str(req.json()['data']['ref_id'])
#                     payment.save()
#                     context = {
#                         'message': f"پرداخت با موفقیت انجام شد، کد رهگیری شما {str(req.json()['data']['ref_id'])}",
#                         'type': 1,
#                     }
#                     return redirect('payments:show_verification_message', context)
#                 elif t_status == 101:
#                     order.is_finally = True
#                     order.save()
#
#                     payment.is_finally = True
#                     payment.status_code = t_status
#                     payment.ref_id = str(req.json()['data']['ref_id'])
#                     payment.save()
#                     context = {
#                         'message': f"پرداخت قبلا انجام شده، کد رهگیری شما {str(req.json()['data']['ref_id'])}",
#                         'type': 1,
#                     }
#                     return redirect('payments:show_verification_message', context)
#                 else:
#                     payment.status_code = t_status
#                     payment.save()
#                     context = {
#                         'message': f"خطا در فرایند پرداخت ، کد وضعیت {t_status}",
#                         'type': 2,
#                     }
#                     return redirect('payments:show_verification_message', context)
#             else:
#                 e_code = req.json()['errors']['code']
#                 e_message = req.json()['errors']['message']
#                 context = {
#                     'message': f"خطا در فرایند پرداخت : Error code : {e_code} , Error message: {e_message} ",
#                     'type': 2,
#                 }
#                 return redirect('payments:show_verification_message', context)
#         else:
#             context = {
#                 'message': 'پرداخت لغو شد',
#                 'type': 2,
#             }
#             return redirect('payments:show_verification_message', context)


# ________________________________________________________________________ test

class ZarinpalPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        amount = order.get_order_total_price()
        description = 'پرداخت از طریق درگاه زرین‌پال انجام شد'
        payment = Payment.objects.create(
            order=order,
            customer=Customer.objects.get(user=request.user),
            amount=amount,
            description=description
        )

        order.is_finally = True
        order.save()

        payment.is_finally = True
        payment.status_code = 100
        payment.ref_id = 12345678910
        payment.save()
        message = f"پرداخت با موفقیت انجام شد، کد رهگیری شما qwe431258"
        type = 1
        return redirect('payments:verify_status', message, type)


# _________________________________________________________________________ show message

def show_verification_message(request, message, type):
    return render(request, 'payments_app/verify_status.html', {'message': message, 'type': type})


# ______________________________________________________ all receipts

class AllReceipts(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_admin:
            payments = Payment.objects.filter(Q(is_finally=True), Q(is_done=False))
            return render(request, 'payments_app/all_receipts.html', {'payments': payments})
        return redirect('main:index')


# ________________________________________________________ user receipt

class UserReceipt(LoginRequiredMixin, View):
    def get(self, request, payment_id):
        flag = False
        user = request.user
        if user.is_admin:
            flag = True
        payment = Payment.objects.get(id=payment_id)
        order = Order.objects.get(order_payments__id=payment_id)
        customer = Customer.objects.get(customer_payments__id=payment_id)
        sub_total_price = 0
        for item in order.orders_details1.all():
            sub_total_price += item.price * item.qty
        order_final_price, delivery, tax = utils.price_by_delivery_tax(sub_total_price, order.discount)
        discount_by_toman = int(sub_total_price * order.discount / 100)

        context = {
            'flag': flag,
            'payment': payment,
            'order': order,
            'customer': customer,
            'sub_total_price': sub_total_price,
            'delivery': delivery,
            'discount_by_toman': discount_by_toman,
            'order_final_price': order_final_price,
        }

        return render(request, 'payments_app/partials/user_receipt.html', context)


def result_receipt(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        payment.is_done = True
        payment.save()
        return redirect('payments:all_receipts')
    except ObjectDoesNotExist:
        message = messages.error(request, 'خطا در انجام عملیات')
        return redirect('main:index')
