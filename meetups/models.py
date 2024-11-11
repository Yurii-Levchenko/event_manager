from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


class Meetups(models.Model):
    title=models.CharField(max_length=200)
    # organizer=models.ForeignKey('Users', null=True, on_delete=models.SET_NULL)
    organizer=models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    slug=models.SlugField(unique=True)
    description=models.TextField()
    image=models.ImageField(upload_to='meetups_images/%Y/%m/%d/')
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
    
    def should_be_archived(self):
        if self.event_date is None:
            return False
        return self.event_date < (timezone.now() + timezone.timedelta(hours=2))

    def archive(self):
        if not self.is_archived:
            self.is_archived = True
            self.save()

class News(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True, null=True, blank=True)
    # author=models.ForeignKey('Users', null=True, on_delete=models.SET_NULL)
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


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        ) 
        user.is_admin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    image=models.ImageField(upload_to='user_images', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # meetups = models.ManyToManyField(Meetups, blank=True)
    # news = models.ManyToManyField(News, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = 'Users'
    
    def full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.full_name()
    
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        
        # Basic check for a specific object
        # if obj is not None and hasattr(obj, 'owner'):
        #     return obj.owner == self  # Allow if the user owns the object
        
        return perm in self.get_all_permissions()
    
    def has_module_perms(self, meetups):
        if self.is_superuser:
            return True
        
        return any(perm.startswith(meetups + '.') for perm in self.get_all_permissions())
    


