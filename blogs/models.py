import uuid
from django.db import models
from accounts.models import User

def short_uuid():
    return str(uuid.uuid4())[:8]  # Take the first 8 characters of the UUID

class Blog(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=short_uuid, editable=False, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title
