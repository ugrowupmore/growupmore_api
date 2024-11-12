# learn/serializers.py

from rest_framework import serializers
from learn.models.subject import Subject
from learn.models.chapter import Chapter
from learn.models.topic import Topic
from learn.models.subtopic import SubTopic


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
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class SubTopicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)
    yt_thumb_image = serializers.ImageField(max_length=200, default="na.png", required=False)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    topic_title = serializers.CharField(source='topic.title', read_only=True)

    class Meta:
        model = SubTopic
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')
