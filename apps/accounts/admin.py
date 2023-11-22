from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer
from .forms import UserCreationForm, UserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['mobile_number', 'name', 'family', 'email', 'is_active', 'is_admin', 'is_superuser',
                    'complete_register']
    list_filter = ['family', 'is_active', 'is_admin', 'groups']
    search_fields = ['mobile_number', 'email', 'name', 'family']
    ordering = ['mobile_number', 'is_active', 'is_admin']
    filter_horizontal = ('groups',)

    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('personal_info', {'fields': ('name', 'family', 'email', 'gender')}),
        ('permissions', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
        ('groups', {'fields': ('groups',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('mobile_number', 'password1', 'password2')}),
        ('personal info', {'fields': ('name', 'family', 'email', 'gender')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_admin'].disabled = True
            form.base_fields['is_active'].disabled = True
            form.base_fields['groups'].disabled = True
        return form


# _______________________________________________________

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'landline_number']
