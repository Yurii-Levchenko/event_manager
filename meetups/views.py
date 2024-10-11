from msilib.schema import ListView
from django.shortcuts import render
from .models import Meetups, News
from django.views.generic import ListView

# Event Management System: Design an event management 
# application that allows users to create, manage, and join events. 
# Include features like event calendars, RSVP management, 
# and notifications for upcoming events.
# also add simple chat for users, usergroups

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
    

# def meetups_page(request):
#     meetups = Meetups.objects.all()

#     return render(request, 'meetups/meetups_page.html', {
#         'show_meetups': True,
#         'meetups': meetups
#     })

def meetup_details(request, meetup_slug):
    selected_meetup = {
        'title': Meetups.objects.get(slug=meetup_slug).title,
        'description': Meetups.objects.get(slug=meetup_slug).description,
        'location': Meetups.objects.get(slug=meetup_slug).location,
        'city': Meetups.objects.get(slug=meetup_slug).city,
        'country': Meetups.objects.get(slug=meetup_slug).country,
        'image': Meetups.objects.get(slug=meetup_slug).image,
        'is_online': Meetups.objects.get(slug=meetup_slug).is_online,
        'link': Meetups.objects.get(slug=meetup_slug).link,
        'is_published': Meetups.objects.get(slug=meetup_slug).is_published
    }

    return render(request, 'meetups/meetup_details.html', {
        'meetup_title': selected_meetup['title'],
        'meetup_description': selected_meetup['description'],
        'meetup_location': selected_meetup['location'],
        'meetup_city': selected_meetup['city'],
        'meetup_country': selected_meetup['country'],
        'meetup_image': selected_meetup['image'],
        'meetup_is_online': selected_meetup['is_online'],
        'meetup_link': selected_meetup['link'],
        'meetup_is_published': selected_meetup['is_published']
    })


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
    pass
