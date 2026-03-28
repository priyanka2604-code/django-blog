from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(status=Post.Status.PUBLISH)
        )

class DraftManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(status=Post.Status.DRAFT)
        )

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISH = 'PB', 'Published'


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    
    body = models.TextField()

    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    objects = models.Manager() # The default manager
    published = PublishedManager() # Our custom manager
    draft = DraftManager() # Our custom manager

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ['-publish']

        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    