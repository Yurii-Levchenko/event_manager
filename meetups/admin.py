from django.contrib import admin
from .models import Meetups, News, Tag, Comment
from django.utils.html import format_html
from django.urls import reverse

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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','author', 'meetup_link', 'created_at', 'updated_at')
    list_display_links = ('id', 'author')
    list_filter = ('updated_at',)
    search_fields = ('author', 'meetup__title')

    @admin.display(description="Meetup")
    def meetup_link(self, obj):
        if obj.meetup:
            url = reverse("admin:meetups_meetups_change", args=[obj.meetup.id]) # <app's name>_<model's name>_change (meetups_meetups_change)
            return format_html('<a href="{}">{}</a>', url, obj.meetup.title)
        return "-"


admin.site.register(Meetups, MeetupsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)