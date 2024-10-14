from django.shortcuts import render
from .models import Meetups, News
from django.views.generic import ListView, View

# Event Management System: Design an event management 
# application that allows users to create, manage, and join events. 
# Include features like event calendars, RSVP management, 
# and notifications for upcoming events.
# also add simple chat for users, usergroups

class MainPageView(View):
    def get(self, request):
        return render(request, 'meetups/index.html')
    


class AllMeetupsView(ListView):
    template_name = 'meetups/meetups_page.html'
    model = Meetups
    ordering = ['event_date']
    context_object_name = 'all_meetups'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_with_date = queryset.exclude(event_date__isnull=True).order_by('event_date')
        queryset_without_date = queryset.filter(event_date__isnull=True).order_by('-created_at')
        return list(queryset_with_date) + list(queryset_without_date)
    
    def archived_meetups(self, request, *args, **kwargs):
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
    

# class ArchivedMeetupsView(ListView):
#     template_name = 'meetups/archived_meetups_page.html'
#     model = Meetups
#     ordering = ['-event_date']
#     context_object_name = 'archived_meetups'


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


