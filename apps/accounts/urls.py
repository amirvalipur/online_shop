from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change_password/', ChangePassView.as_view(), name='change_password'),
    path('remember_password/', RememberPassView.as_view(), name='remember_password'),

    path('user_panel/', UserPanelView.as_view(), name='user_panel'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('show_last_payments/', show_last_payments, name='show_last_payments'),
]
