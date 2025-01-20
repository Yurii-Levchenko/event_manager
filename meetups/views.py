from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Meetups, News
from django.views.generic import ListView, View
from django.utils import timezone
from django.db.models import Q

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import MeetupForm


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
        queryset_with_date = Meetups.objects.filter(
            is_published=True, is_archived=False, event_date__isnull=False
        ).order_by('event_date')
        
        queryset_without_date = Meetups.objects.filter(
            is_published=True, is_archived=False, event_date__isnull=True
        ).order_by('-created_at')
        
        return queryset_with_date | queryset_without_date
    
    def get_queryset(self):    
        if self.request.path == '/archive':
            return Meetups.objects.filter(is_published=True, is_archived=True).order_by('event_date')
        queryset = self.get_ordered_meetups()
        
        tag = self.request.GET.get('tag')
        is_online = self.request.GET.get('is_online')
        search = self.request.GET.get('search')
        
        if tag:
            queryset = queryset.filter(tags__caption__icontains=tag)
        
        if is_online:
            queryset = queryset.filter(is_online=is_online.lower() == 'true')
        
        # Search by title, city, or country
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(city__icontains=search) |
                Q(country__icontains=search)
            )
        
        return queryset
    
    def archived_meetups(self, request):
        archived_meetups = self.get_queryset().filter(is_archived=True)
        return render(request, 'meetups/archived_meetups.html', {'archived_meetups': archived_meetups})
    
    def get_template_names(self):
        if self.request.path == '/archive':
            return ['meetups/archived_meetups_page.html']
        return ['meetups/meetups_page.html']


class MeetupsDetailView(View):
    def going(self, request, meetup_id):
        going_meetups = request.session.get("going_meetups")
        if going_meetups is not None:
            going = meetup_id in going_meetups
        else:
            going = False
        return going

    def get(self, request, meetup_slug):
        meetup = Meetups.objects.get(slug=meetup_slug)

        context = {
            'meetup': meetup,
            'meetup_tags': meetup.tags.all(),
            'going': self.going(request, meetup.id)
        }
        return render(request, 'meetups/meetup_details.html', context)
    

@method_decorator(login_required, name='dispatch')
class GoingView(View):
    def get(self, request):
        going_meetups = request.session.get("going_meetups", [])
        
        meetups = Meetups.objects.filter(id__in=going_meetups) if going_meetups else []
        context = {
            "meetups": meetups,
            "has_meetups": bool(meetups),
            "user": request.user
        }
        return render(request, "meetups/going.html", context)
    
    def post(self, request):
        going_meetups = request.session.get("going_meetups", [])

        meetup_id = int(request.POST["meetup_id"])

        if meetup_id in going_meetups:
            going_meetups.remove(meetup_id)
        else:
            going_meetups.append(meetup_id)
        
        request.session["going_meetups"] = going_meetups
        return HttpResponseRedirect("/going")


# class GoingView(View):
#     def get(self, request):
#         going_meetups = request.session.get("going_meetups")
#         context = {}

#         if going_meetups is None or len(going_meetups) == 0:
#             context["meetups"] = []    
#             context["has_meetups"] = False
#         else:
#             meetups = Meetups.objects.filter(id__in=going_meetups)
#             context["meetups"] = meetups
#             context["has_meetups"] = True
#         return render(request, "meetups/going.html", context)
    
#     def post(self, request):
#         going_meetups = request.session.get("going_meetups")

#         if going_meetups is None:
#             going_meetups = []
        
#         meetup_id = int(request.POST["meetup_id"])

#         if meetup_id not in going_meetups:
#             # im adding meetup's id, not object as a whole
#             going_meetups.append(meetup_id)
#         else:
#             going_meetups.remove(meetup_id)
        
#         request.session["going_meetups"] = going_meetups
#         return HttpResponseRedirect("/going")
        # return redirect('going')
    

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


def calendar_view(request):
    return render(request, 'meetups/calendar.html')



@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('meetups.add_meetups', raise_exception=True), name='dispatch')
class MeetupCreateView(CreateView):
    form_class = MeetupForm
    template_name = 'meetups/meetup_create.html'

    def get_success_url(self):
        return reverse('meetups:meetups')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.organizer = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('meetups.change_meetups', raise_exception=True), name='dispatch')
class MeetupUpdateView(UpdateView):
    model = Meetups
    form_class = MeetupForm
    template_name = 'meetups/meetup_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'meetup_slug'

    def get_success_url(self):
        return reverse('meetups:meetup-details', kwargs={'meetup_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_text'] = 'Update Meetup'
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('meetups.delete_meetups', raise_exception=True), name='dispatch')
class MeetupDeleteView(DeleteView):
    model = Meetups
    slug_field = 'slug'
    slug_url_kwarg = 'meetup_slug'
    success_url = reverse_lazy('meetups:meetups')
