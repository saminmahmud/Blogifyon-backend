from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import Comment, Reply
from .serializers import CommentSerializer, ReplySerializer
from rest_framework.filters import SearchFilter, OrderingFilter
User = get_user_model()

class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            return Comment.objects.filter(post=post_id)
        return Comment.objects.all()

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = []
    permission_classes = []

