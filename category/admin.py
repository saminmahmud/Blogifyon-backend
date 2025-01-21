from django.contrib import admin
from .models import Category
from unfold.admin import ModelAdmin

class CategoryAdmin(ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)
