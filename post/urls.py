from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('list', views.PostView) 
router.register('create_post', views.CreatePostView, basename="create_post") 
router.register('likes', views.LikeViewSet)
router.register('category_post', views.CategoryPost, basename="category_post")
router.register('saved_post', views.SavedPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]