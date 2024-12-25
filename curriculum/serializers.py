
# curriculum/serializers.py

from rest_framework import serializers

from curriculum.models.course import Course
from curriculum.models.module import Module
from curriculum.models.subject import Subject
from curriculum.models.chapter import Chapter
from curriculum.models.syllabus import Syllabus
from curriculum.models.topic import Topic
from curriculum.models.subtopic import Subtopic

from curriculum.models.course_category import CourseCategory
from curriculum.models.course_subcategory import CourseSubCategory


class SubjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)
    yt_thumb_image = serializers.ImageField(max_length=200, default="na.png", required=False)

    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class ChapterSerializer(serializers.ModelSerializer):
    yt_thumb_image = serializers.ImageField(max_length=200, default="na.png", required=False)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class TopicSerializer(serializers.ModelSerializer):
    yt_thumb_image = serializers.ImageField(max_length=200, default="na.png", required=False)    
    chapter_name= serializers.CharField(source='chapter.name', read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class SubTopicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)
    yt_thumb_image = serializers.ImageField(max_length=200, default="na.png", required=False)    
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = Subtopic
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class CourseSubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='course_category.category', read_only=True)   

    class Meta:
        model = CourseSubCategory
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class CourseSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(max_length=200, default="na.png", required=False)    
    sub_category_name = serializers.CharField(source='course_subcategory.sub_category', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class ModuleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class SyllabusSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    module_name = serializers.CharField(source='module.module_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = Syllabus
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')