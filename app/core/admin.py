from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id','email','name']
    fieldsets = (
        (None,{'fields': ['email','password']}),
        ('Personal Information',{'fields': ['name']}),
        ('Permissions',{'fields': ['is_active','is_staff','is_superuser']}),
        ('Important Dates',{'fields': ['last_login']})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password','password2','email',),            
        }),
    )

admin.site.register(models.User,UserAdmin)