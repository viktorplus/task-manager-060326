
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.projects.models import Project
class AllProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'created_at')


class CreateProjectSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ('title', 'description', 'created_at')

    def validate_description(self, value: str) -> str:
        if len(value) < 30:
            raise serializers.ValidationError("Description must be at least 30 characters long")
        return value


class ProjectDetailSerializer(ModelSerializer):
    count_of_files = serializers.IntegerField(source='file_count', read_only=True)
    class Meta:
        model = Project
        fields = ('title', 'description', 'created_at', 'count_of_files')


class ProjectShortInfoSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title')