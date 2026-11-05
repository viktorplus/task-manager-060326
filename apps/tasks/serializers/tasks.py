from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.tasks.models import Task, Tag
from .tags import TagSerializer
from ...projects.models import Project

"""Задача 2: Задачи для проекта, сотрудник с пагинацией, создание
задачи
1. В приложении tasks, в модуле serializers создайте новый файл
tasks_serializers.py.
2. Реализуйте сериализатор AllTasksSerializer для отображения краткой
информации о задачах. Поля для отображения:
● name
● status
● priority
● project (название проекта)
● assignee (email сотрудника)
● deadline
3. Реализуйте сериализатор CreateTaskSerializer для создания новой задачи.
Поля для создания новой задачи:
● name
● description
● priority
● project(заполняется не по id, а по имени проекта)
● tags
● deadline
4. Добавьте в сериализатор на создание новой задачи валидаторы полей:
● name (минимальная длина)
● description (минимальная длина)
● priority (передаётся строго число, переданное число должно быть в
доступных choices, от 1 до 5)
● project (передаётся имя проекта, поиск среди всех проектов. Если
такого имени нет - выводить сообщение об ошибке, что проекта не
существует)
● tags (список имён тегов, поиск среди всех тегов. Если тега по имени
найдено не было - выводить сообщение об ошибке)
● deadline (не может быть в прошлом)
5. Переопределите метод create для добавления информации тегов в
промежуточную таблицу.
6. Напишите класс-отображение AllTasksListAPIView для получения списка всех
задач, привязанных к конкретному проекту, или сотруднику на выбор.
Реализуйте пагинацию для отображения только первых пяти записей на одной
странице. Добавьте метод post для создания задачи.
7. Зарегистрируйте новый эндпоинт, проверьте как отрабатывают запросы GET,
POST.
8. Зафиксируйте все изменения, сделайте запрос на слияние"""

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority']


class TaskInfoSerializer(ModelSerializer):
    tag = TagSerializer( many=True) # source='tag' - если поле в модели называется иначе, то указываем source='имя_поля_в_модели'
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'tag', 'project', 'created_at', 'updated_at', 'due_date']

class AllTasksSerializer(ModelSerializer):
    project = serializers.CharField(source='project.title')
    assignee = serializers.CharField(source='assignee.email', allow_null=True)
    due_date = serializers.DateTimeField(source='due_date')

    class Meta:
        model = Task
        fields = ['title', 'status', 'priority', 'project', 'assignee', 'due_date']

class CreateTaskSerializer(ModelSerializer):
    project = serializers.SlugRelatedField(slug_field='title', queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'project', 'tags', 'due_date']


    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value

    def validate_priority(self, value):
        if value not in [choice[0] for choice in Task.Priority.choices]:
            raise serializers.ValidationError("Priority must be one of the available choices.")
        return value

    def validate_project(self, value):
        from apps.projects.models import Project
        try:
            project = Project.objects.get(title=value)
        except Project.DoesNotExist:
            raise serializers.ValidationError(f"Project with title '{value}' does not exist.")
        return project

    def validate_tags(self, value):
        from apps.tasks.models import Tag
        tags = []
        for tag_name in value:
            try:
                tag = Tag.objects.get(name=tag_name)
                tags.append(tag)
            except Tag.DoesNotExist:
                raise serializers.ValidationError(f"Tag with name '{tag_name}' does not exist.")
        return tags

    def validate_due_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        task.tag.set(tags_data)
        task.save()
        return task