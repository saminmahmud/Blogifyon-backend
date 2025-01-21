from django.contrib import admin
from .models import Notification
from unfold.admin import ModelAdmin

admin.site.register(Notification, ModelAdmin)

