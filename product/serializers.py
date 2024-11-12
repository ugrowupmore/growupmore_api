# product/serializers.py

from rest_framework import serializers
from product.models.course import Course
from product.models.course_module import CourseModule
from product.models.course_syllabus import CourseSyllabus
from product.models.recommended_course import RecommendedCourse


class CourseSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(max_length=200, default="na.png", required=False)
    course_category_name = serializers.CharField(source='course_category.category', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.sub_category', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class CourseModuleSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseModule
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class CourseSyllabusSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    module_name = serializers.CharField(source='module.module_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    topic_title = serializers.CharField(source='topic.title', read_only=True)

    class Meta:
        model = CourseSyllabus
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class RecommendedCourseSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    recommended_course_title = serializers.CharField(source='recommended_course.title', read_only=True)

    class Meta:
        model = RecommendedCourse
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')
