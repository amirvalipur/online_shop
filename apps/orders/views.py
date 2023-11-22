from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

import utils
from apps.products.models import Product
from .shop_cart import ShopCart
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from .models import Order, OrderDetails, PaymentType
from .forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist
from apps.discounts.forms import CouponForm
from apps.discounts.models import Coupon
from django.db.models import Q
from datetime import datetime
from django.contrib import messages


class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        context = {
            'shop_cart': shop_cart
        }
        return render(request, 'orders_app/shop_cart.html', context)


def show_shop_cart(request):
    shop_cart = ShopCart(request)
    total_price = shop_cart.calc_total_price()
    order_final_price, delivery, tax = utils.price_by_delivery_tax(total_price)

    context = {
        'shop_cart': shop_cart,
        'shop_cart_count': shop_cart.count,
        'total_price': total_price,
        'delivery': delivery,
        'tax': tax,
        'order_final_price': order_final_price,
    }
    return render(request, 'orders_app/partials/show_shop_cart.html', context)


# ______________________________________________ ajax/add_to_shop_cart

def add_to_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    product = get_object_or_404(Product, id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.add_to_shop_cart(product, qty)
    return HttpResponse("ok")


def delete_from_shop_cart(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')


def update_shop_cart(request):
    product_id_list = request.GET.getlist('product_id_list[]')
    qty_list = request.GET.getlist('qty_list[]')
    shop_cart = ShopCart(request)
    shop_cart.update(product_id_list, qty_list)
    return redirect('orders:show_shop_cart')


def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        shop_cart = ShopCart(request)
        if shop_cart.count == 0:
            messages.warning(request, 'سبد خرید شما خالی می باشد', 'warning')
            return redirect('orders:shop_cart')

        try:
            customer = Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer = Customer.objects.create(user=request.user)

        order = Order.objects.create(customer=customer)

        for item in shop_cart:
            OrderDetails.objects.create(
                order=order,
                product=item['product'],
                price=item['final_price'],
                qty=item['qty']
            )

        return redirect('orders:checkout_order', order_id=order.id)


# _________________________________________________________

class CheckOutOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        shop_cart = ShopCart(request)
        order = get_object_or_404(Order, id=order_id)
        total_price = shop_cart.calc_total_price()
        order_final_price, delivery, tax = utils.price_by_delivery_tax(total_price, order.discount)
        discount_by_toman = 0
        if order.discount > 0:
            discount_by_toman = int(total_price * order.discount / 100)

        data = {
            'name': user.name,
            'family': user.family,
            'email': user.email,
            'landline_number': customer.landline_number,
            'address': customer.address,
            'description': order.description,
            'payment_type': order.payment_type,
        }

        form = OrderForm(data)
        form_coupon = CouponForm()
        context = {
            'shop_cart': shop_cart,
            'shop_cart_count': shop_cart.count,
            'total_price': total_price,
            'delivery': delivery,
            'tax': tax,
            'order_final_price': order_final_price,
            'discount_by_toman': discount_by_toman,
            'order': order,
            'form': form,
            'form_coupon': form_coupon,
        }

        return render(request, 'orders_app/checkout.html', context)

    def post(self, request, order_id):
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                order = Order.objects.get(id=order_id)
                order.description = data['description']
                order.payment_type = PaymentType.objects.get(id=data['payment_type'])
                order.save()

                user = request.user
                user.name = data['name']
                user.family = data['family']
                user.email = data['email']
                user.save()

                customer = Customer.objects.get(user=user)
                customer.landline_number = data['landline_number']
                customer.address = data['address']
                customer.save()
                messages.success(request, 'اطلاعات با موفقیت ثبت شد', 'success')
                return redirect('payments:verify_zarinpal_payment', order_id)

            except ObjectDoesNotExist:
                messages.error(request, 'فاکتوری با این مشخصات یاف نشد', 'danger')
                return redirect('orders:checkout', order_id)
        return redirect('orders:checkout', order_id)


# ___________________________________

class ApplayCouponView(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            cd = coupon_form.cleaned_data
            coupon_code = cd['coupon_code']

        coupon = Coupon.objects.filter(
            Q(coupon_code=coupon_code),
            Q(is_active=True),
            Q(start_date__lte=datetime.now()),
            Q(end_date__gte=datetime.now()),
        )

        discount = 0
        try:
            order = Order.objects.get(id=order_id)
            if coupon:
                discount = coupon[0].discount
                order.discount = discount
                order.save()
                messages.success(request, 'تخفیف با موفقیت اعمال شد', 'success')
                return redirect('orders:checkout_order', order_id)
            else:
                order.discount = discount
                order.save()
                messages.error(request, 'کد وارد شده معتبر نمی باشد', 'danger')
        except ObjectDoesNotExist:
            messages.error(request, 'سفارش موجود نیست')
        return redirect('orders:checkout_order', order_id)
