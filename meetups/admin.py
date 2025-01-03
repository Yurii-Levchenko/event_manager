from django.contrib import admin
from .models import Meetups, News, Tag
# Register your models here.

class MeetupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'organizer', 'country', 'city','is_online', 'is_published', 'is_archived')
    prepopulated_fields = {'slug': ('title', 'organizer')}
    list_display_links = ('id', 'title')
    list_filter = ('country', 'is_online', 'is_published', 'is_archived')
    search_fields = ('title', 'organizer', 'country', 'city')

    fieldsets = (
        (None, {'fields': ('title', 'organizer', 'tags', 'slug')}),
        ('Info', {'fields': ( 'description', 'image', 'event_date')}),
        ('Location', {'fields': ('is_online', 'link', 'country', 'city', 'location')}),
        ('Status', {'fields': ('is_published', 'is_archived')}),
    )

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'updated_at', 'created_at', 'is_published')
    prepopulated_fields = {'slug': ('title', 'author')}
    # prepopulated_fields = {'slug': ('title', 'author__name', 'author__surname')}
    list_display_links = ('id', 'title')
    list_filter = ('author', 'is_published')
    search_fields = ('title', 'author')

    fieldsets = (
        (None, {'fields': ('title', 'author', 'slug', 'image')}),
        ('Content', {'fields': ( 'description', 'content')}),
        ('Status', {'fields': ('is_published',)}),
    )

class TagAdmin(admin.ModelAdmin):
    list_display = ('caption',)

# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'surname', 'email', 'is_active')
#     list_display_links = ('id', 'name', 'surname')
#     list_filter = ('is_active',)
#     search_fields = ('name', 'surname', 'email')

admin.site.register(Meetups, MeetupsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Users, UsersAdmin)