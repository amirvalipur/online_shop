from django.urls import path
from .views import *

app_name = 'search'

urlpatterns = [
    path('search_view/', SearchResultView.as_view(), name='search_view')
]