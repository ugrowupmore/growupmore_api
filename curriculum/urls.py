# curriculum/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet, ChapterViewSet, TopicViewSet, SubTopicViewSet,
    CourseCategoryViewSet, CourseSubCategoryViewSet, CourseViewSet,
    ModuleViewSet, SyllabusViewSet
)


router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'subtopics', SubTopicViewSet, basename='subtopic')
router.register(r'course-categories', CourseCategoryViewSet, basename='coursecategory')
router.register(r'course-subcategories', CourseSubCategoryViewSet, basename='coursesubcategory')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'syllabus', SyllabusViewSet, basename='syllabus')

urlpatterns = [
    path('', include(router.urls)),
]
