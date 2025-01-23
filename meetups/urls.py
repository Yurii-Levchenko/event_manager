from django.urls import path
from . import views

app_name = 'meetups'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('meetups', views.AllMeetupsView.as_view(), name='meetups'),
    path('meetups/<slug:meetup_slug>', views.MeetupsDetailView.as_view(), name='meetup-details'),
    path('archive', views.AllMeetupsView.as_view(), name='archived-meetups'),
    path('news', views.AllNewsView.as_view(), name='news'),
    path('news/<slug:news_slug>', views.NewsDetailView.as_view(), name='news-details'),
    path('going/', views.GoingView.as_view(), name="going"),
    path('meetups/create/', views.MeetupCreateView.as_view(), name='meetup-create'),
    path('meetups/<slug:meetup_slug>/update/', views.MeetupUpdateView.as_view(), name='meetup-update'),
    path('meetups/<slug:meetup_slug>/delete/', views.MeetupDeleteView.as_view(), name='meetup-delete'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('meetups/<slug:meetup_slug>/comment/', views.add_comment, name='add-comment'),
]