from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    slug = models.SlugField(max_length=250)
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

    class Meta:
        # This ordering will apply by default for database queries when no specific order is provided in the query |   ##(-)hyphen indicates descending order before the field name, -publish.
        
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
    
    def __str__(self):
        return self.title