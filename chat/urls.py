from django.urls import path, include
from chat import views as chat_views

urlpatterns = [
    # path("chat/", chat_views.ChatPageView.as_view(), name="chat-page"),
    path("chat/", chat_views.chatPage, name="chat-page"),
]

# <slug:meetup_slug>/