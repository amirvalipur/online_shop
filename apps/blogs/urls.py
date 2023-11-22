from django.urls import path, include
from .views import *

app_name = 'blogs'
urlpatterns = [
    path('blogs_list/', BlogsListView.as_view(), name='blogs_list'),
    path('blog_details/<slug:slug>/', BlogDetailsView.as_view(), name='blog_details'),
    path('last_blog/', last_blog, name='last_blog'),
]