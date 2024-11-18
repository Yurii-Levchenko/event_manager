from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from meetups.models import Meetups, News, Tag
from accounts.models import CustomUser
from .serializers import CustomUserSerializer, MeetupSerializer, NewsSerializer, TagSerializer
from rest_framework.filters import SearchFilter

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomUserListAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(email__icontains=email)
        return queryset
    
    @staticmethod
    def get_extra_actions():
        return []

class MeetupsRestView(viewsets.ModelViewSet):
    queryset = Meetups.objects.all()
    serializer_class = MeetupSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['city', 'country', 'is_online']
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'city', 'country']

class NewsRestView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

class TagsRestView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer