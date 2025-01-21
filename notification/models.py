from django.db import models
from author.models import Author
from post.models import Post

class Notification(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='notification')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id})  Notification for --> {self.user}'
    
    class Meta:
        ordering = ['-created_at']