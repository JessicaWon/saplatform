from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import SkyUser
from .forms import SkyUserChangeForm, SkyUserCreationForm

class SkyUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'phone_number', 'mobile_number',
                                         'zip_code', 'home_address',
                                         'bank_id_first', 'bank_id_last')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = SkyUserChangeForm
    add_form = SkyUserCreationForm
    list_display = ('email', 'first_name', 'last_name',
                    'mobile_number', 'phone_number',
                    'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'mobile_number', 'phone_number')
    ordering = ('email',)

admin.site.register(SkyUser, SkyUserAdmin)
