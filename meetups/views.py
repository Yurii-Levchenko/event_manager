from django.shortcuts import render
from .models import Meetups, News
from django.views.generic import ListView, View
from django.utils import timezone


# Event Management System: Design an event management 
# application that allows users to create, manage, and join events. 
# Include features like event calendars, RSVP management, 
# and notifications for upcoming events.
# also add simple chat for users, usergroups

class MainPageView(View):
    def get(self, request):
        recent_meetups = AllMeetupsView.get_ordered_meetups()[:5]
        recent_news = News.objects.filter(is_published=True).order_by('-created_at')[:5]

        context = {
            'all_meetups': recent_meetups,
            'all_news': recent_news,
        }

        return render(request, 'meetups/index.html', context)


class AllMeetupsView(ListView):
    template_name = 'meetups/meetups_page.html'
    model = Meetups
    ordering = ['event_date']
    context_object_name = 'all_meetups'
    
    @classmethod
    def get_ordered_meetups(cls):
        # queryset = super().get_queryset()
        queryset = Meetups.objects.filter(is_published=True, is_archived=False)
        queryset_with_date = queryset.exclude(event_date__isnull=True).order_by('event_date')
        queryset_without_date = queryset.filter(event_date__isnull=True).order_by('-created_at')
        return list(queryset_with_date) + list(queryset_without_date)
    
    def get_queryset(self):
        return self.get_ordered_meetups()
    
    def archived_meetups(self, request):
        archived_meetups = self.get_queryset().filter(is_archived=True)
        return render(request, 'meetups/archived_meetups.html', {'archived_meetups': archived_meetups})
    
    def get_template_names(self):
        if self.request.path == '/archive':
            return ['meetups/archived_meetups_page.html']
        return ['meetups/meetups_page.html']


class MeetupsDetailView(View):
    def get(self, request, meetup_slug):
        meetup = Meetups.objects.get(slug=meetup_slug)

        context = {
            'meetup': meetup,
        }
        return render(request, 'meetups/meetup_details.html', context)
    

class AllNewsView(ListView):
    template_name = 'meetups/news_page.html'
    model = News
    ordering = ['-created_at']
    context_object_name = 'all_news'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:2]
        return data


class NewsDetailView(ListView):
    def get(self, request, news_slug):
        news = News.objects.get(slug=news_slug)

        context = {
            'news': news,
        }
        return render(request, 'meetups/news_details.html', context)

