from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Pathway(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pathways")
    title = models.CharField(max_length=200)
    description = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES, default='public')

    upvotes = models.PositiveIntegerField(default=0)  
    downvotes = models.PositiveIntegerField(default=0) 

    @property
    def votes(self):
        return self.upvotes - self.downvotes
    
class Comment(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    depth = models.PositiveIntegerField(default=1)


class ImageResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="image_resources")
    title = models.CharField(max_length=200)
    notes = models.TextField()
    image = models.ImageField(upload_to='resources/')
    created_at = models.DateTimeField(auto_now_add=True)

class LinkResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="link_resources")
    title = models.CharField(max_length=200)
    notes = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class TextResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="text_resources")
    title = models.CharField(max_length=200)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)

class FileResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="file_resources")
    title = models.CharField(max_length=200)
    notes = models.TextField()
    attachment = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)
