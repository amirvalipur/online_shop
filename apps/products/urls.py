from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('cheapest_products/', get_cheapest_products, name='cheapest_products'),
    path('last_products/', get_last_products, name='last_products'),
    path('popular_products/', get_popular_products, name='popular_products'),
    path('product_detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('related_products/<slug:slug>/', get_related_products, name='related_products'),
    path('products_list/<slug:slug>/', ProductsList.as_view(), name='products_list'),
    path('ajax_admin/', get_filter_value_for_feature, name='filter_value_for_feature'),
    path('product_groups_filter/', get_product_groups, name='product_groups_filter'),
    path('brand_filter/<slug:slug>/', get_brand, name='brand_filter'),
    path('features_filter/<slug:slug>/', get_features, name='features_filter'),
]
