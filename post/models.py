from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from author.models import Author
from category.models import Category
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Like(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.id}) {self.user} liked --> post: {self.post}'
    
# @receiver(post_save, sender=Like)
@receiver(post_save)
def create_like_notification(sender, instance, created, **kwargs):
    if created and sender.__name__ == 'Like':

        from notification.models import Notification
        notification = Notification.objects.create(
            user=instance.post.author,
            post=instance.post,
            content=f'{instance.user.user.username} liked on your post-"{instance.post.title}".',
        )
        post = instance.post
        post.likes = Like.objects.filter(post=post).count()
        post.save()

        # Send notification through channels
        notification_data = {
            'user': {
                'id': instance.user.id,
                'username': instance.user.user.username,  
                'email': instance.user.user.email,  
                'profile_picture_url': instance.user.profile_picture_url  
            },
            'post': {
                'id': instance.post.id,
                'title': instance.post.title,
                'content': instance.post.content,
                'created_at': instance.post.created_at.isoformat(),
                'author': {
                    'id': instance.post.author.id,
                    'username': instance.post.author.user.username,  
                    'profile_picture_url': instance.post.author.profile_picture_url  
                },
            },
            'content': f'{instance.user.user.username} liked your post: "{instance.post.title}".',
            'created_at': notification.created_at.isoformat(), 
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{instance.post.author.user.username}-{instance.post.author.id}",
            {
                'type': 'send_notification',
                'notification': notification_data
            }
        )


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post')
    categories = models.ManyToManyField(Category)
    post_image_url = models.ImageField(upload_to='title_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['-created_at']

        
class SavedPost(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}) User: {self.user.user.username} --> Post: {self.post.title}'

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']