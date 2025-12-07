from django.contrib import admin
from .models import CustomerUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomerUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'city', 'state', 'address', 'phone'),
        }),
    )
    
admin.site.register(CustomerUser, CustomerUserAdmin)