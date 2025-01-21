from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Like, SavedPost
from .serializers import CreatePostSerializer, PostSerializer, LikeSerializer, SavedPostSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['post__id']
    authentication_classes = []
    permission_classes = []

class CategoryPost(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['categories__name']
    ordering_fields = ['likes', 'created_at']

class SavedPostViewSet(viewsets.ModelViewSet):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['user__id']


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['author__user__username', 'title']
    ordering_fields = ['likes', 'created_at']
    authentication_classes = []
    permission_classes = []

class CreatePostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer

