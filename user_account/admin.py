from django.contrib import admin
from .models import CustomUser
# from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

# admin.site.register(CustomUser, UserAdmin)