from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.CustomUserListAPIView)
router.register('meetups', views.MeetupsRestView)
router.register('news', views.NewsRestView)
router.register('tags', views.TagsRestView)


urlpatterns = [
    path('', include(router.urls)),
    path('calendar/', views.calendar_events, name='calendar-events'),
]