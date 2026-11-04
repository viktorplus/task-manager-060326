from typing import Any

from django.utils import timezone
from rest_framework import serializers

from apps.projects.models import Project
from apps.tasks.models import Task, Tag


class AllTasksSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(read_only=True, slug_field='title')
    assignee = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Task
        fields = ('id', 'title', 'project', 'status', 'assignee', 'due_date', 'priority',)


class CreateTaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Project.objects.all(),
        error_messages={'does_not_exist': 'Project with that title does not exist'},
    )
    tag = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        error_messages={'does_not_exist': 'Tag with that name does not exist'},
    )

    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'project', 'tag', 'due_date')

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('The title of the task cant be less than 10 characters long')
        return value

    def validate_description(self, value):
        if len(value) < 50:
            raise serializers.ValidationError('The description of the task cant be less than 50 characters long')
        return value

    def validate_priority(self, value):
        if value not in Task.Priority.values:
            raise serializers.ValidationError(f'Priority must be one of {Task.Priority.values}')
        return value

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('The deadline of the task cant be in the past')
        return value

    def create(self, validated_data: dict[str, Any]) -> Task:
        tags = validated_data.pop('tag', [])
        task = Task.objects.create(**validated_data)
        task.tag.set(tags)  # запись тегов в промежуточную таблицу
        return task