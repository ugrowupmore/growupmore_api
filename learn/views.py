# learn/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from learn.models.subject import Subject
from learn.models.chapter import Chapter
from learn.models.topic import Topic
from learn.models.subtopic import SubTopic
from .serializers import (
    SubjectSerializer, ChapterSerializer, TopicSerializer, SubTopicSerializer
)
from utils.pagination import KendoPagination


# Subject ViewSet
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('subject_code').all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'short_name', 'subject_code', 'status', 'is_active']
    search_fields = ['name', 'short_name', 'subject_code']
    ordering_fields = '__all__'
    ordering = ['name']


# Chapter ViewSet
class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.select_related('subject').all()
    serializer_class = ChapterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'status', 'is_active']
    search_fields = ['title']
    ordering_fields = '__all__'
    ordering = ['title']


# Topic ViewSet
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.select_related('subject', 'chapter').all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'chapter', 'status', 'is_active']
    search_fields = ['title']
    ordering_fields = '__all__'
    ordering = ['title']


# SubTopic ViewSet
class SubTopicViewSet(viewsets.ModelViewSet):
    queryset = SubTopic.objects.select_related('subject', 'chapter', 'topic').all()
    serializer_class = SubTopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'chapter', 'topic', 'status', 'is_active']
    search_fields = ['title']
    ordering_fields = '__all__'
    ordering = ['title']
