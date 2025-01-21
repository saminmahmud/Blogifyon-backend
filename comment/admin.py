from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Comment, Reply

admin.site.register(Comment,ModelAdmin)
admin.site.register(Reply, ModelAdmin)
