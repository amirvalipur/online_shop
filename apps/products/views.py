from django.shortcuts import render, get_object_or_404
from .models import *
from .filters import *
from django.db.models import Q, Count, Min, Max
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator


# ______________________________________________________________ ارزان ترین محصولات
def get_cheapest_products(request, *args, **kwargs):
    accept_group = ProductGroup.objects.filter(Q(is_active=True))
    products = Product.objects.filter(Q(is_active=True), Q(product_group__in=accept_group)).order_by('price')
    final_products = list(dict.fromkeys(products))[:6]
    product_groups = ProductGroup.objects.filter(Q(group_parent=None))
    context = {
        'products': final_products,
        'product_groups': product_groups
    }
    return render(request, 'products_app/partials/cheapest_products.html', context)


# ______________________________________________________________ جدید ترین محصولات
def get_last_products(request, *args, **kwargs):
    accept_group = ProductGroup.objects.filter(Q(is_active=True))
    products = Product.objects.filter(Q(is_active=True), Q(product_group__in=accept_group)).order_by('-publish_date')
    final_products = list(dict.fromkeys(products))[:6]
    product_groups = ProductGroup.objects.filter(Q(group_parent=None))
    context = {
        'products': final_products,
        'product_groups': product_groups
    }
    return render(request, 'products_app/partials/last_products.html', context)


# ______________________________________________________________ محبوب ترین گروه ها
def get_popular_products(request, *args, **kwargs):
    product_groups = ProductGroup.objects.filter(Q(is_active=True)).annotate(
        count=Count('products_of_group')).order_by('-count').filter(~Q(group_parent=None))
    context = {
        'product_groups': product_groups
    }
    return render(request, 'products_app/partials/popular_products.html', context)


# _________________________________________________________________________________ product detail

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        product_group = product.product_group.filter(Q(is_active=True))
        return render(request, 'products_app/product_detail.html', {'product': product, 'product_group': product_group})


# ___________________________________________________________________________________ related_products

def get_related_products(request, *args, **kwargs):
    related_list = []
    current_products = get_object_or_404(Product, slug=kwargs['slug'])
    groups = current_products.product_group.all().filter(Q(is_active=True))
    for group in groups:
        related_list.extend(
            Product.objects.filter(Q(is_active=True), Q(product_group=group), ~Q(id=current_products.id)))
        related_list = list(dict.fromkeys(related_list))
    return render(request, 'products_app/partials/related_products.html', {'related_list': related_list})


# ______________________________________________________________________________ filter/product groups
def get_product_groups(request):
    product_groups = ProductGroup.objects.annotate(count=Count('products_of_group')).filter(
        Q(is_active=True), ~Q(count=0)).order_by('-count')
    return render(request, 'products_app/partials/product_groups.html', {'product_groups': product_groups})


# ______________________________________________________________________________ filter/brand
def get_brand(request, **kwargs):
    if kwargs['slug'] == 'all-product':
        brands = Brand.objects.all()
    else:
        current_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
        brand_list_id = current_group.products_of_group.filter(Q(is_active=True)).values('brand_id')
        brands = Brand.objects.filter(Q(pk__in=brand_list_id)).annotate(count=Count('products_of_brand')).filter(
            ~Q(count=0)).order_by('-count')
    return render(request, 'products_app/partials/brand_filter.html', {'brands': brands})


# ________________________________________________________________________________ filter/ features
def get_features(request, **kwargs):
    current_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    list_features = current_group.features_of_product_group.all()
    feature_dict = dict()
    for feature in list_features:
        feature_dict[feature] = feature.feature_values.all()
    return render(request, 'products_app/partials/features_filter.html', {'feature_dict': feature_dict})


# ______________________________________________________________________________ ajax/filter value
def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id = request.GET['feature_id']
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)


# _______________________________________________________________________________ products list
class ProductsList(View):

    def get(self, request, **kwargs):
        flag = False
        if kwargs['slug'] == 'all-product':
            products = Product.objects.filter(Q(is_active=True))
            current_group = None
        else:
            current_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
            products = Product.objects.filter(Q(is_active=True), Q(product_group=current_group))
            flag = True

        # price filter range
        range_price = products.aggregate(min=Min('price'), max=Max('price'))
        show_current_price = request.GET.get('price')
        if not show_current_price:
            show_current_price = range_price.get('max')

        if int(show_current_price) != int(range_price.get('max')):
            flag = True

        # filter by price
        price_filter = ProductFilter(request.GET, queryset=products)
        products = price_filter.qs

        # filter by brand
        brand_filter = request.GET.getlist('brand')
        if brand_filter:
            products = products.filter(brand__id__in=brand_filter)
            flag = True

        # filter by faeture
        feature_filter = request.GET.getlist('feature')
        if feature_filter:
            products = products.filter(product_of_features__filter_value__id__in=feature_filter).distinct()
            flag = True

        # paginator
        show_number = request.GET.get('show_number')
        if not show_number:
            product_per_page = 6
            show_number = str(product_per_page)
        else:
            product_per_page = int(show_number)

        paginator = Paginator(products, product_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = products.count()
        group_slug = kwargs['slug']

        context = {
            'flag': flag,
            'products': products,
            'product_group': current_group,
            'range_price': range_price,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'show_number': show_number,
            'show_current_price': show_current_price,
        }
        return render(request, 'products_app/products_list.html', context)
