from django.urls import path
from . import views

urlpatterns = [
    path('meetups', views.AllMeetupsView.as_view(), name='meetups'),
    path('meetups/<slug:meetup_slug>', views.MeetupsDetailView.as_view(), name='meetup-details'),
    path('archive', views.AllMeetupsView.as_view(), name='archived-meetups'),
    path('news', views.AllNewsView.as_view(), name='news'),
    path('news/<slug:news_slug>', views.NewsDetailView.as_view(), name='news-details'),
]