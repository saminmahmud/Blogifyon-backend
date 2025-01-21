from rest_framework import serializers
from .models import Comment, Reply


class ReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['id', 'comment', 'reply_comment', 'post', 'author', 'author_username', 'content', 'created_at', 'replies']

    def get_replies(self, obj):
        nested_replies = Reply.objects.filter(reply_comment=obj)
        serializer = ReplySerializer(nested_replies, many=True)
        return serializer.data
    
    def get_author_username(self, obj):
        return obj.author.user.username

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'replies']

    def get_replies(self, obj):
        direct_replies = Reply.objects.filter(comment=obj, reply_comment__isnull=True)
        serializer = ReplySerializer(direct_replies, many=True)
        return serializer.data
    
    def get_author_username(self, obj):
        return obj.author.user.username
    
