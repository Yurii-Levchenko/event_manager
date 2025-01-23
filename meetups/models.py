from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Meetups(models.Model):
    title=models.CharField(max_length=200)
    organizer=models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    slug=models.SlugField(unique=True)
    tags = models.ManyToManyField('Tag', blank=True)
    description=models.TextField()
    image=models.ImageField(upload_to='meetups_images/%Y/%m/%d/', default='default.jpeg')
    event_date=models.DateTimeField(blank=True, null=True)
    is_online=models.BooleanField(default=False)
    link=models.URLField(blank=True)
    country=models.CharField(max_length=200, blank=True)
    city=models.CharField(max_length=200, blank=True)
    location=PlainLocationField(based_fields=['city'], zoom=7, default='49,24', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_published=models.BooleanField(default=False)
    is_archived=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Meetups'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.organizer.id}")
        super().save(*args, **kwargs)

    def should_be_archived(self):
        if self.event_date is None:
            return False
        return self.event_date < (timezone.now() + timezone.timedelta(hours=2))

    def archive(self):
        if not self.is_archived:
            self.is_archived = True
            self.save()
    
    def clean(self):
        if self.is_published:
            if not self.title or not self.organizer or not self.event_date:
                raise ValidationError("Please fill in all required fields before publishing.")
        super().clean()

class News(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True, null=True, blank=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    image=models.ImageField(upload_to='news_images/%Y/%m/%d/', null=True, blank=True)
    description=models.TextField()
    content=RichTextUploadingField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_published=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'News'


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Comment(models.Model):
    meetup = models.ForeignKey(Meetups, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.full_name()} on {self.meetup.title}"


