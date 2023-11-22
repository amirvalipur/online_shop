from django.contrib import admin
from .models import *
from django.db.models import Count, Q
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description
from jalali_date.admin import ModelAdminJalaliMixin


# ____________________________________________________________________ brand
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_title', 'count_product']
    list_filter = ['brand_title', ]
    search_fields = ['brand_title', ]
    ordering = ['brand_title', ]

    def get_queryset(self, request):
        qs = Brand.objects.annotate(sub_brand=Count('products_of_brand'))
        return qs

    def count_product(self, obj):
        return obj.sub_brand


# ____________________________________________________________________ product group
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    extra = 1


def deactive_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    if res == 1:
        message = 'گروه انتخابی غیر فعال شد'
    else:
        message = 'گروه های انتخابی غیر فعال شدند'
    modeladmin.message_user(request, message)


def active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    if res == 1:
        message = 'گروه انتخابی فعال شد'
    else:
        message = 'گروه های انتخابی فعال شدند'
    modeladmin.message_user(request, message)


# _____________________________
class GroupFilter(SimpleListFilter):
    title = 'گروه محصولات'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        sub_group = ProductGroup.objects.filter(~Q(groups=None))
        return [(item.id, item.group_title) for item in sub_group]

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset


# _____________________________


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ['group_title', 'is_active', 'group_parent', 'sub_group', 'count_product']
    # list_filter = (('group_parent', RelatedDropdownFilter), ('is_active', DropdownFilter))
    list_filter = (GroupFilter,)
    search_fields = ['group_title', ]
    ordering = ['group_title', 'is_active']
    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [deactive_product_group, active_product_group]
    list_editable = ['is_active']

    def get_queryset(self, request):
        return ProductGroup.objects.annotate(number_of_sub=Count('products_of_group'))

    @short_description('تعداد کالا ها')
    def count_product(self, obj):
        return obj.number_of_sub

    @short_description('زیر گروه ها')
    def sub_group(self, obj):
        return [items.group_title for items in obj.groups.filter(Q(is_active=True))]


# ________________________________________________________________ product
class ProductFeatureInstanceInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 5

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/my_script.js',
        )


class ProductGalleryInstanceInlineAdmin(admin.TabularInline):
    model = ProductGallery


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['product_name', 'is_active', 'groups_product', 'brand']
    list_filter = (
        ('product_group', RelatedDropdownFilter), ('is_active', DropdownFilter), ('brand', RelatedDropdownFilter))
    search_fields = ['product_name', ]
    ordering = ['product_name', 'is_active']
    filter_horizontal = ['product_group']
    inlines = [ProductFeatureInstanceInlineAdmin, ProductGalleryInstanceInlineAdmin]
    list_editable = ['is_active']

    fieldsets = (
        (None, {'fields': ('product_name', 'image_name', 'summery_description', 'description')}),
        (None, {'fields': (('brand', 'is_active'), 'product_group')}),
        (None, {'fields': ('price', 'slug', 'publish_date')}),
    )
    @short_description('گروه های کالا')
    def groups_product(self, obj):
        return [items for items in obj.product_group.filter(Q(is_active=True))]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# ________________________________________________________ feature
class FeatureValueInstanceInlineAdmin(admin.TabularInline):
    model = FeatureValue



@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['feature_name', 'display_feature_groups', 'display_feture_values']
    list_filter = (
        ('product_group', RelatedDropdownFilter), ('feature_name', DropdownFilter))
    search_fields = ['feature_name', ]
    ordering = ['feature_name']
    filter_horizontal = ['product_group']
    inlines = [FeatureValueInstanceInlineAdmin]

    @short_description('گروه های ویژگی')
    def display_feature_groups(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])

    @short_description('مقادیر ویژگی')
    def display_feture_values(self, obj):
        return ', '.join([value.value_title for value in obj.feature_values.all()])


