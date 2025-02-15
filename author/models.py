from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed 
from django.dispatch import receiver
from PIL import Image

from django.contrib.auth import get_user_model
User = get_user_model()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/" ,blank=True, null=True, default='profile_pictures/default_pic.jpg')
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    post_count = models.PositiveIntegerField(default=0)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

    def update_post_count(self):
        from post.models import Post
        self.post_count = Post.objects.filter(author=self).count()
        self.save()

    # image optimization
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with Image.open(self.profile_picture.path) as img:
            target_size =300
            if img.height > target_size or img.width > target_size:
                output_size = (target_size, target_size)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

@receiver(post_save)
def update_post_count_on_post_save(sender, instance, **kwargs):
    if sender.__name__ == 'Post':
        author = instance.author
        if author:
            author.update_post_count()


@receiver(post_delete)
def update_post_count_on_post_delete(sender, instance, **kwargs):
    if sender.__name__ == 'Post':
        author = instance.author
        if author:
            author.update_post_count()


@receiver(m2m_changed, sender=Author.followers.through)
def create_follow_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        from notification.models import Notification
        for follower_id in pk_set:
            if instance.user.id != follower_id:  
                follower = Author.objects.get(id=follower_id)
                message = f'{follower.user.username} has started following you.'
                Notification.objects.create(
                    user=instance,
                    content=message
                )

                # Send notification through channels
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"{instance.user.username}-{instance.user.id}",
                    {
                        'type': 'send_notification',
                        'notification': {
                            'user': {
                                'id': follower.user.id,
                                'username': follower.user.username,
                                'profile_picture_url': follower.profile_picture_url,
                            },
                            'content': f'{follower.user.username} has started following you.',
                        }
                    }
                )



STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    reviewer = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reviews')
    reviewed_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reviews_received')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    
    def __str__(self):
        return f"Reviewer: {self.reviewer.user.username}; Reviewed Author: {self.reviewed_author.user.username}"
    
    class Meta:
        ordering = ['-created']
    

@receiver(post_save)
def create_review_notification(sender, instance, created, **kwargs):
    if created and sender.__name__ == 'Review':
        from notification.models import Notification
        Notification.objects.create(
            user=instance.reviewed_author,
            content=f'You received a new review from {instance.reviewer.user.username}.',
        )

        # Send notification through channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{instance.reviewed_author.user.username}-{instance.reviewed_author.user.id}",
            {
                'type': 'send_notification',
                'notification': {
                    "user": {
                        "id": instance.reviewer.id,
                        "username": instance.reviewer.user.username,
                        "profile_picture_url": instance.reviewer.profile_picture_url,
                    },
                    "content": f'You received a new review from {instance.reviewer.user.username}.',
                    "rating": instance.rating,
                    "body": instance.body,
                }
            }
        )

