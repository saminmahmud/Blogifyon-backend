from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('list', views.AuthorView) 
router.register('reviews', views.ReviewView) 
router.register('profile', views.AuthorProfileViewSet, basename='profile') 
# router.register('send_email', views.SendEmailToAuthorView, basename='send_email') 

urlpatterns = [
    path('', include(router.urls)),
    path('send_email/', views.send_email_to_author_view.as_view()),
]
