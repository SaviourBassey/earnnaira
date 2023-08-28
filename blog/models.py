from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class PostCategory(models.Model):
    category = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}"


class Post(models.Model):
    post_title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)
    post_category = models.ManyToManyField(PostCategory)
    # post_tags
    post_image = models.ImageField()
    post_body = RichTextField(blank=True, null=True)
    likes = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now_add=True)

    def snippet(self):
        return f"{self.post_body}"[:200] + "..."

    def __str__(self):
        return f"{self.post_title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.post_title)  # Auto-populate the slug
        super().save(*args, **kwargs)


class PostShare(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
