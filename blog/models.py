from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

#Custom object manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)

#Post Model 
class Post(models.Model):
    
    class Status(models.TextChoices):
        PUBLISHED = 'PB', 'Published'
        DRAFT = 'DF', 'Draft'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #Status of a post can be either be Draft--> DF or Published--> PB
    status = models.CharField(max_length=2,choices=Status.choices, default=Status.DRAFT)
    
    """We use related_name to specify the name of the reverse relationship, from User to Post. This will
    allow us to access related objects easily from a user object by using the user.blog_posts notation. """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    
    #Objects Manager
    objects = models.Manager() #default manager
    published = PublishedManager() #Custom object manager
    
    tags=TaggableManager()

    class Meta:
        # This ordering will apply by default for database queries when no specific order is provided in the query |   ##(-)hyphen indicates descending order before the field name, -publish.
        
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", 
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ] )

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
        return f"Comment by {self.name} on {self.post}"
    