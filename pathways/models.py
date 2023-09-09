from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
import os, cloudinary.uploader

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

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="comment_replies", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)


class ImageResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="image_resources")
    title = models.CharField(max_length=200)
    notes = models.TextField()
    image = models.ImageField(upload_to='resources/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class LinkResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="link_resources")
    title = models.CharField(max_length=200)
    notes = models.TextField()
    url = models.URLField()
    fetched_title = models.CharField(max_length=512, blank=True, null=True)
    fetched_image_url = models.URLField(blank=True, null=True)
    fetched_domain = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class TextResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="text_resources")
    title = models.CharField(max_length=200)
    content = HTMLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class FileResource(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="file_resources")
    title = models.CharField(max_length=200)
    notes = models.TextField()
    attachment = models.FileField(upload_to='files/')
    name = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    cloudinary_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if 'DYNO' in os.environ:
            if self.attachment and (not self.cloudinary_url or self.attachment.name != self.name):
                ext = self.attachment.name.split('.')[-1].lower()
                image_types = ['jpg', 'jpeg', 'png', 'gif']
                raw_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'csv']

                if ext in image_types:
                    resource_type = 'image'
                elif ext in raw_types:
                    resource_type = 'raw'
                else:
                    resource_type = 'raw'

                uploaded_file = cloudinary.uploader.upload(
                    self.attachment.file,
                    resource_type=resource_type
                )
                
                self.cloudinary_url = uploaded_file['url']
                self.name = self.attachment.name

        super().save(*args, **kwargs)

class StudyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)

@receiver(post_save, sender=StudyTask)
def create_revisions(sender, instance, **kwargs):
    if instance.is_completed and not Revision.objects.filter(study_task=instance).exists():
        Revision.objects.create(
            study_task=instance,
            pathway=instance.pathway,
            revision_type=Revision.FIRST,
            due_date=date.today() + timedelta(days=1)
        )
        

class Revision(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    REVISION_STATUS = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]

    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'
    FOURTH = 'fourth'
    REVISION_TYPE = [
        (FIRST, 'First Revision'),
        (SECOND, 'Second Revision'),
        (THIRD, 'Third Revision'),
        (FOURTH, 'Fourth Revision'),
    ]

    study_task = models.ForeignKey(StudyTask, on_delete=models.CASCADE, related_name='revisions')
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="revisions")
    revision_type = models.CharField(max_length=10, choices=REVISION_TYPE)
    status = models.CharField(max_length=10, choices=REVISION_STATUS, default=PENDING)
    due_date = models.DateField()

    @property
    def progress_percentage(self):
        return {
            self.FIRST: 25,
            self.SECOND: 50,
            self.THIRD: 75,
            self.FOURTH: 100
        }.get(self.revision_type, 0)
    
class FollowedPathway(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name="followers")
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'pathway']


