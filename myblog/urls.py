from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('theboss/', admin.site.urls),
    path('accounts/', include('user_account.urls')),
    path('author/', include('author.urls')),
    path('category/', include('category.urls')),
    path('post/', include('post.urls')),
    path('comment-reply/', include('comment.urls')),
    path('notification/', include('notification.urls')),

    path("ckeditor/", include("ckeditor_uploader.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
