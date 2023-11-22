from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import *
from .forms import *
from .models import CustomUser, Customer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from apps.payments.models import Payment


class UserRegisterView(View):
    template_name = 'accounts_app/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserRegisterForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            active_code = create_random_code(3)
            CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                password=data['password1'],
                active_code=active_code,
            )
            send_sms(receptor=data['mobile_number'], active_code=active_code,
                     message=f'کد تایید شما : {active_code}')
            request.session['user_session'] = {
                'mobile_number': data['mobile_number'],
                'active_code': str(active_code),
                'remember_password': False,
                'inside': False,
            }
            messages.info(request, 'کد ارسال شده را وارد کنید', 'info')
            return redirect('accounts:verify')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
            return redirect('accounts:register')


# _______________________________________________________________________
class UserVerifyView(View):
    template_name = 'accounts_app/verify.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserVerifyForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserVerifyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            if user_session['active_code'] == data['active_code']:
                if not user_session['remember_password']:
                    user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                    user.is_active = True
                    user.complete_register = True
                    active_code = create_random_code(3)
                    user.active_code = active_code
                    user.save()
                    del request.session['user_session']
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        messages.success(request, 'ثبت نام با موفقیت انجام شد', 'success')
                        return redirect(next_url)
                    else:
                        messages.success(request, 'ثبت نام با موفقیت انجام شد', 'success')
                        return redirect('main:index')

                else:
                    return redirect('accounts:change_password')

            else:
                messages.error(request, 'کد وارد شده صحیح نمی باشد', 'danger')
                return redirect('accounts:verify')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
            return redirect('accounts:verify')


# _______________________________________________________________________
class UserLoginView(View):
    template_name = 'accounts_app/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserLoginForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if CustomUser.objects.filter(mobile_number=data['mobile_number']).exists():
                db_user = CustomUser.objects.get(mobile_number=data['mobile_number'])
                if not db_user.is_active:
                    if db_user.complete_register:
                        messages.error(request,
                                       'حساب کاربری شما از سوی ادمین سایت غیر فعال شده لطفا به آیدی پشتیبان پیام دهید',
                                       'danger')
                        return redirect('accounts:login')
                    active_code = create_random_code(3)
                    request.session['user_session'] = {
                        'mobile_number': data['mobile_number'],
                        'active_code': str(active_code),
                        'remember_password': False
                    }
                    db_user.active_code = active_code
                    db_user.save()
                    send_sms(receptor=data['mobile_number'], active_code=active_code,
                             message=f'کد تایید شما : {active_code}')
                    messages.warning(request, 'جهت فعالسازی شماره تلفن ، کد پیامک شده را وارد کنید', 'warning')
                    return redirect('accounts:verify')
                else:
                    user = authenticate(username=data['mobile_number'], password=data['password'])
                    if user is not None:
                        login(request, user)
                        next_url = request.GET.get('next')
                        if next_url:
                            messages.success(request, 'ورود با موفقیت انجام شد', 'success')
                            return redirect(next_url)
                        else:
                            messages.success(request, 'ورود با موفقیت انجام شد', 'success')
                            return redirect('main:index')
                    else:
                        messages.error(request, 'نام کاربری یا رمز عبور اشتباه می باشد', 'danger')
                        return render(request, self.template_name, {'form': form})
            else:
                messages.error(request, 'شماره تلفن وارد شده یافت نشد لطفا ابتدا ثبت نام کنید', 'danger')
                return redirect('accounts:register')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
            return redirect('main:index')


# _______________________________________________________________________
class UserLogoutView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        session_data = request.session['shop_cart']
        logout(request)
        request.session['shop_cart'] = session_data
        return redirect('main:index')


# _______________________________________________________________________
class ChangePassView(View):
    template_name = 'accounts_app/change_password.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['user_session'] = {
                'mobile_number': request.user.mobile_number,
                'inside': True,
            }
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = ChangePassForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChangePassForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user_session = request.session['user_session']
                user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                user.set_password(data['password2'])
                user.active_code = create_random_code(3)
                user.save()
                if user_session['inside']:
                    messages.success(request, 'رمز عبور باموفقیت تغییر کرد', 'success')
                    login(request, user)
                    return redirect('accounts:user_panel')
                else:
                    del request.session['user_session']
                    messages.success(request, 'رمز عبور باموفقیت تغییر کرد', 'success')
                    return redirect('accounts:login')
            except:
                messages.warning(request, 'ابتدا شماره همراه خود را وارد کنید', 'warning')
                return redirect('accounts:remember_password')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
            return redirect('accounts:change_password')


# _______________________________________________________________________
class RememberPassView(View):
    template_name = 'accounts_app/remember_password.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RememberPassForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RememberPassForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = CustomUser.objects.get(mobile_number=data['mobile_number'])
            active_code = create_random_code(3)
            user.active_code = active_code
            user.save()
            send_sms(receptor=data['mobile_number'], active_code=active_code,
                     message=f'کد تایید شما : {active_code}')
            request.session['user_session'] = {
                'mobile_number': data['mobile_number'],
                'active_code': str(active_code),
                'remember_password': True,
                'inside': False
            }
            return redirect('accounts:verify')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
            return redirect('main:index')


# __________________________________________________________________ user_panel

class UserPanelView(LoginRequiredMixin, View):
    template_name = 'accounts_app/userpanel.html'

    def get(self, request):
        user = request.user
        flag = False
        if user.is_admin:
            flag = True
        try:
            customer = Customer.objects.get(user=request.user)
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'landline_number': customer.landline_number,
                'address': customer.address,
                'image': customer.image_name,
            }
        except ObjectDoesNotExist:
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
            }
        return render(request, self.template_name, {'user_info': user_info, 'flag': flag})


# ________________________________________________________________

class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        flag = False
        if user.is_admin:
            flag = True
        try:
            customer = Customer.objects.get(user=request.user)
            initial_dict = {
                'mobile_number': user.mobile_number,
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'landline_number': customer.landline_number,
                'address': customer.address,
            }
            image_url = customer.image_name
        except ObjectDoesNotExist:
            initial_dict = {
                'mobile_number': user.mobile_number,
                'name': user.name,
                'family': user.family,
                'email': user.email,
            }
            image_url = False
        form = UpdateProfileForm(initial=initial_dict)
        return render(request, 'accounts_app/update_profile.html', {'form': form, 'image_url': image_url, 'flag': flag})

    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            user.name = cd['name']
            user.family = cd['family']
            user.email = cd['email']
            user.save()
            try:
                customer = Customer.objects.get(user=request.user)
                customer.landline_number = cd['landline_number']
                customer.address = cd['address']
                customer.image_name = cd['image']
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=user,
                    landline_number=cd['landline_number'],
                    address=cd['address'],
                    image_name=cd['image']
                )
            messages.success(request, 'ویراش پروفایل با موفقیت انجام شد', 'success')
            return redirect('accounts:user_panel')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی‌باشد', 'danger')
            return render(request, 'accounts_app/update_profile.html', {'form': form})


# ________________________________________________________________


@login_required
def show_last_payments(request):
    payments = Payment.objects.filter(customer_id=request.user.id).order_by('-register_datetime')[:6]
    return render(request, 'accounts_app/partials/show_last_payments.html', {'payments': payments})

    # ________________________________________________________________
