from django import forms


class CouponForm(forms.Form):
    coupon_code = forms.CharField(label='',
                                  error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'کد تخفیف'})
                                  )
