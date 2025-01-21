from django.db import models
from author.models import Author
from post.models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import Notification

from django.contrib.auth import get_user_model
User = get_user_model()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id})  Comment by: {self.author} --> post: {self.post}'
    
    class Meta:
        ordering = ['-created_at']

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        person = instance.author
        title = instance.post.title
        Notification.objects.create(
            user=instance.post.author,
            post=instance.post,
            content=f'{person} commented on your post-"{title}".',
        )

        # Send notification through channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(  
            f"{instance.post.author.user.username}-{instance.post.author.id}",
            {
                'type': 'send_notification',
                'notification': {
                    'user': {
                        'id': instance.author.id,
                        'username': instance.author.user.username,
                        'profile_picture_url': instance.author.profile_picture_url,
                    },
                    'post': {
                        'id': instance.post.id,
                        'title': instance.post.title,
                    },
                    'content': f'{person} commented on your post-"{title}".',
                }
            }
        )


class Reply(models.Model):
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    reply_comment = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.comment:
            return f'{self.id})  Reply by: {self.author} --> Comment: {self.comment.id}'
        elif self.reply_comment:
            return f'{self.id}) Reply by: {self.author} --> Reply: {self.reply_comment.id}'
        
    class Meta:
        ordering = ['created_at']

@receiver(post_save, sender=Reply)
def create_reply_notification(sender, instance, created, **kwargs):
    if created:
        person = instance.author
        title = instance.post.title
        if instance.comment and instance.reply_comment is None:
            Notification.objects.create(
                user=instance.comment.author,
                post=instance.post,
                content=f'{person} replied on your comment in post-"{title}".',
            )

            # Send notification through channels
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"{instance.comment.author.user.username}-{instance.comment.author.id}",
                {
                    'type': 'send_notification',
                    'notification': {
                        "user": {
                            'id': instance.author.id,
                            'username': instance.author.user.username,
                            'profile_picture_url': instance.author.profile_picture_url,
                        },
                        "post": {
                            'id': instance.post.id,
                            'title': instance.post.title,
                        },
                        "content": f'{person} replied on your comment in post-"{title}".',
                    }
                }
            )

        if instance.reply_comment and instance.comment is None:
            Notification.objects.create(
                user=instance.reply_comment.author,
                post=instance.post,
                content=f'{person} replied on your comment in post-"{title}".',
            )

            # Send notification through channels
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"{instance.reply_comment.author.user.username}-{instance.reply_comment.author.id}",
                {
                    'type': 'send_notification',
                    'notification': {
                        "user": {
                            'id': instance.author.id,
                            'username': instance.author.user.username,
                            'profile_picture_url': instance.author.profile_picture_url,
                        },
                        "post": {
                            'id': instance.post.id,
                            'title': instance.post.title,
                        },
                        "content": f'{person} replied on your reply in post-"{title}".',
                    }
                }
            )
