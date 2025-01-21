from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('theboss/', admin.site.urls),
    path('accounts/', include('user_account.urls')),
    path('author/', include('author.urls')),
    path('category/', include('category.urls')),
    path('post/', include('post.urls')),
    path('comment-reply/', include('comment.urls')),
    path('notification/', include('notification.urls')),
]
