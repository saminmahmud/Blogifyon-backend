from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

router.register('comment', CommentViewSet, basename='comment')
router.register('reply', ReplyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('post/<int:post_id>/', CommentViewSet.as_view({'get': 'list'}), name='comment-list-by-post'),
    path('<int:pk>/', CommentViewSet.as_view({'get': 'retrieve'}), name='comment-detail'),
]