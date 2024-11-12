# learn/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet, ChapterViewSet, TopicViewSet, SubTopicViewSet
)

# Registering the ViewSets with the router
router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'subtopics', SubTopicViewSet, basename='subtopic')

# Including router URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
