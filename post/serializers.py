from rest_framework import serializers

from author.serializers import AuthorSummarySerializer
from category.serializers import CategorySerializer
from .models import Post, Like, SavedPost

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    author = AuthorSummarySerializer(read_only=True) 

    class Meta:
        model = Post
        fields = '__all__'
     

class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class SavedPostSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all()) 
    post_details = serializers.SerializerMethodField()

    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post', 'post_details', 'created_at']

    def get_post_details(self, obj):
        serializer = PostSerializer(obj.post)
        post_data = serializer.data
        
        if post_data.get('post_image_url'):
            post_data['post_image_url'] = self.context['request'].build_absolute_uri(post_data['post_image_url'])
        
        return post_data