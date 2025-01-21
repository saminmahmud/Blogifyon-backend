from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # post = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ['id', 'user', 'post', 'content', 'is_read', 'created_at']

    # def get_user(self, obj):
    #     return obj.user.user.username
    # def get_post(self, obj):
    #     return obj.post.title if obj.post else None
    
