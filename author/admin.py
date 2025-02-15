from django.contrib import admin
from .models import Author, Review

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'user__email',  'join_date', 'post_count')
    
admin.site.register(Author, AuthorAdmin)

admin.site.register(Review)
