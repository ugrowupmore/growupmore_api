# product/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    CourseModuleViewSet,
    CourseSyllabusViewSet,
    RecommendedCourseViewSet
)

# Registering the ViewSets with the router
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'course-modules', CourseModuleViewSet, basename='course-module')
router.register(r'course-syllabuses', CourseSyllabusViewSet, basename='course-syllabus')
router.register(r'recommended-courses', RecommendedCourseViewSet, basename='recommended-course')

# Including router URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
