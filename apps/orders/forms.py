from django import forms
from .models import PaymentType


class OrderForm(forms.Form):
    name = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'نام'}),
                           error_messages={'required': 'این فیلد نمیتواند خالی بماند'}
                           )

    family = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={'class': 'input input-bordered w-full', 'placeholder': 'نام خانوادگی'}),
                             error_messages={'required': 'این فیلد نمیتواند خالی بماند'}
                             )
    email = forms.CharField(label='',
                            widget=forms.EmailInput(
                                attrs={'class': 'input input-bordered w-full', 'placeholder': 'ایمیل'}),
                            required=False
                            )

    landline_number = forms.CharField(label='',
                                      widget=forms.TextInput(
                                          attrs={'class': 'input input-bordered w-full',
                                                 'placeholder': 'شماره تلفن ثابت'}),
                                      required=False
                                      )

    address = forms.CharField(label='',
                              widget=forms.Textarea(
                                  attrs={'class': 'input input-bordered w-full', 'placeholder': 'آدرس', 'rows': 4, }),
                              error_messages={'required': 'این فیلد نمیتواند خالی بماند'},
                              )
    description = forms.CharField(label='',
                                  widget=forms.Textarea(
                                      attrs={'class': 'input input-bordered w-full', 'placeholder': 'توضیحات',
                                             'rows': 4}),
                                  required=False
                                  )

    payment_type = forms.ChoiceField(label='',
                                     choices=[(item.pk, item) for item in PaymentType.objects.all()],
                                     widget=forms.RadioSelect(
                                         attrs={'class': 'radio radio-warning font-YekanBakh-ExtraBold'})
                                     )
