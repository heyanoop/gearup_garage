from django.contrib import admin
from .models import account
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class Account_Admin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'joined_date', 'is_active',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display_links = ('email', 'first_name', 'last_name')
    ordering = ('-joined_date',)
    readonly_fields = ('last_login', 'joined_date')
    
    
admin.site.register(account,Account_Admin)

