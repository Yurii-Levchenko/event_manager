from django.urls import path
from . import views

urlpatterns = [
    path('meetups', views.meetups_page, name='meetups'),
    path('meetups/<slug:meetup_slug>', views.meetup_details, name='meetup-details'),
]