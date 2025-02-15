from django.contrib import admin
from .models import Post, Like, SavedPost

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'created_at', 'updated_at', 'views', 'likes')
    
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(SavedPost)