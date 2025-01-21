from rest_framework import serializers
from user_account.serializers import UserAccountSerializer
from .models import Author, Review
from notification.serializers import NotificationSerializer
from notification.models import Notification

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    unread_notifications = serializers.SerializerMethodField()
    # followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = UserAccountSerializer()

    class Meta:
        model = Author
        fields = [
            'id', 'user', 'profile_picture_url', 'bio', 'address', 
            'twitter', 'facebook', 'linkedin', 'join_date', 
            'post_count', 'unread_notifications', 'followers', 'following'
        ]

    def get_unread_notifications(self, obj):
        notifications = Notification.objects.filter(user=obj.user.id, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return len(serializer.data)

    # def get_user(self, obj):
    #     return obj.user.username

    # def get_followers(self, obj):
    #     # Serialize the followers
    #     followers = obj.followers.all()
    #     return [follower.id for follower in followers]

    def get_following(self, obj):
        # Serialize the following
        following = obj.following.all()
        return [follow.id for follow in following]
    

class SendEmailToAuthorSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required = True)
    sender_id = serializers.IntegerField(required = True)
    content = serializers.CharField(max_length=1000)

    def validate(self, data):
        author_id = data.get('author_id')
        sender_id = data.get('sender_id')
        content = data.get('content')

        if author_id == sender_id:
            raise serializers.ValidationError("Author and sender cannot be the same.")
        if not content.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        
        return data



# for post 
class AuthorSummarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Author
        fields = ['id', 'user']
        
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
        }