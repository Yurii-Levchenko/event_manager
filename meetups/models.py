from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Meetups(models.Model):
    title=models.CharField(max_length=200)
    organizer=models.ForeignKey('Users', on_delete=models.CASCADE)
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

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Meetups'
    
    def is_archived(self):
        if self.event_date is None:
            return False
        return self.event_date < (timezone.now() + timezone.timedelta(hours=2))

    def archive(self):
        self.is_archived = True
        self.save()

class News(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True, null=True, blank=True)
    author=models.ForeignKey('Users', on_delete=models.CASCADE)
    image=models.ImageField(upload_to='news_images/%Y/%m/%d/', null=True, blank=True)
    description=models.TextField()
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
    image=models.ImageField(upload_to='user_images')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # meetups_organized = models.ManyToManyField(Meetups, blank=True)
    # news_written = models.ManyToManyField(News, blank=True)
    
    def full_name(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.full_name()
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    class Meta:
        verbose_name_plural = 'Users'
