from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=20, label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'name', 'family', 'email', 'gender']

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن با هم مغایرت دارند')
        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# _______________________________________________________________________
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href=../password > فراموشی رمز عبور <a/>")

    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'password', 'name', 'family', 'email', 'gender', 'is_active', 'is_admin',
                  'is_superuser']


# _______________________________________________________________________

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={'class': "input input-bordered w-full my-2", 'placeholder': 'رمز عبور را وارد کنید'})
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "input input-bordered w-full my-2", 'placeholder': 'تکرار رمز عبور را وارد کنید'}))

    class Meta:
        model = CustomUser
        fields = ['mobile_number']
        widgets = {'mobile_number': forms.TextInput(
            attrs={'class': "input input-bordered w-full my-2", 'placeholder': 'شماره همراه را وارد کنید'})}

    def clean_password(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن با هم مغایرت دارند')
        return pass2


# _______________________________________________________________________
class UserVerifyForm(forms.Form):
    active_code = forms.CharField(
        error_messages={'required': 'این فیلد نمیتواند خالی باشد'},
        widget=forms.TextInput(
            attrs={'class': "input input-bordered w-full my-2", 'placeholder': 'کد دریافتی را وارد کنید'})
    )


# _______________________________________________________________________
class UserLoginForm(forms.Form):
    mobile_number = forms.CharField(label='شماره همراه', widget=forms.TextInput(
        attrs={'class': 'input input-bordered w-full my-2', 'placeholder': 'شماره همراه را وارد کنید'}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'input input-bordered w-full my-2', 'placeholder': 'رمز عبور را وارد کنید'}))


# _______________________________________________________________________
class ChangePassForm(forms.Form):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'input input-bordered w-full my-2', 'placeholder': 'رمز عبور را وارد کنید'}))
    password2 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'input input-bordered w-full my-2', 'placeholder': 'تکرار رمز عبور را وارد کنید'}))

    def clean_password(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن با هم مغایرت دارند')
        return pass2


# _______________________________________________________________________
class RememberPassForm(forms.Form):
    mobile_number = forms.CharField(label='شماره همراه', widget=forms.TextInput(
        attrs={'class': 'input input-bordered w-full my-2', 'placeholder': 'شماره موبایل را وارد کنید'}))


# _______________________________________________________________________
class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full rounded-xl", "placeholder": "شماره موبایل را وارد کنید",
                   'readonly': 'readonly'})
    )
    name = forms.CharField(
        label="نام",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full rounded-xl", "placeholder": "نام را وارد کنید"})
    )
    family = forms.CharField(
        label="نام خانوادگی",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full rounded-xl", "placeholder": "نام خانوادگی را وارد کنید"})
    )
    email = forms.EmailField(required=False,
        label="ایمیل",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.EmailInput(
            attrs={"class": "input input-bordered w-full rounded-xl", "placeholder": "ایمیل را وارد کنید"})
    )
    landline_number = forms.CharField(required=False,
                                      label="شماره تلفن",
                                      error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
                                      widget=forms.TextInput(
                                          attrs={"class": "input input-bordered w-full rounded-xl",
                                                 "placeholder": "شماره تلفن را وارد کنید"})
                                      )
    address = forms.CharField(
        label="آدرس",
        error_messages={"required": "این فیلد نمی‌تواند خالی باشد"},
        widget=forms.Textarea(
            attrs={"class": "input input-bordered w-full rounded-xl", "placeholder": "آدرس را وارد کنید", 'rows': '3'})
    )
    image = forms.ImageField(required=False)
