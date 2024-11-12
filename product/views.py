# product/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from product.models.course import Course
from product.models.course_module import CourseModule
from product.models.course_syllabus import CourseSyllabus
from product.models.recommended_course import RecommendedCourse
from .serializers import (
    CourseSerializer, CourseModuleSerializer,
    CourseSyllabusSerializer, RecommendedCourseSerializer
)


# Course ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related(
        'course_category',
        'sub_category'
    ).all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'code', 'title', 'level', 'course_category', 'sub_category',
        'has_certification', 'status', 'is_active'
    ]
    search_fields = ['code', 'title', 'tags']
    ordering_fields = '__all__'
    ordering = ['code']


# CourseModule ViewSet
class CourseModuleViewSet(viewsets.ModelViewSet):
    queryset = CourseModule.objects.select_related(
        'course'
    ).all()
    serializer_class = CourseModuleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'module_name', 'status', 'is_active']
    search_fields = ['module_name']
    ordering_fields = '__all__'
    ordering = ['module_name']


# CourseSyllabus ViewSet
class CourseSyllabusViewSet(viewsets.ModelViewSet):
    queryset = CourseSyllabus.objects.select_related(
        'course',
        'module',
        'subject',
        'chapter',
        'topic'
    ).all()
    serializer_class = CourseSyllabusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'course', 'module', 'subject', 'chapter', 'topic',
        'status', 'is_active'
    ]
    search_fields = []
    ordering_fields = '__all__'
    ordering = ['course']


# RecommendedCourse ViewSet
class RecommendedCourseViewSet(viewsets.ModelViewSet):
    queryset = RecommendedCourse.objects.select_related(
        'course',
        'recommended_course'
    ).all()
    serializer_class = RecommendedCourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'recommended_course', 'priority', 'status', 'is_active']
    search_fields = ['description']
    ordering_fields = '__all__'
    ordering = ['priority']
