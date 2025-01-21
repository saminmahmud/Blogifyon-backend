from django.contrib import admin
from .models import Post, Like, SavedPost
from unfold.admin import ModelAdmin

class PostAdmin(ModelAdmin):
    list_display = ('id','title', 'author', 'created_at', 'updated_at', 'views', 'likes')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Like, ModelAdmin)
admin.site.register(SavedPost, ModelAdmin)