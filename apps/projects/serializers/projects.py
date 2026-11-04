
"""Задание 10
1. Установите модуль djangorestframework.
2. Добавить этот модуль в файл requirements.txt.
3. Добавить этот модуль в список установленных приложений в файле settings.py.
4. Создать новый пакет serializers, в котором создать первый файл - projects
5. Импортируйте класс ModelSerializer.
6. Напишите первый сериализатор, который будет обрабатывать поля id и name для проекта,
выдавая общую базу для вывода всех проектов.


Задача 1: Получение, обновление и удаление проекта
1. Создайте новый сериализатор ProjectDetailSerializer для получения
конкретной информации по проекту:
○ name
○ description
○ created_at
○ count_of_files

2. Напишите новый класс-отображение ProjectDetailAPIView для получения
конкретного проекта, обновления и удаления проекта.
3. При обновлении полученного проекта добавьте возможность частичного
обновления полей.
4. Зарегистрируйте новый эндпоинт, проверьте как отрабатывают запросы GET,
PUT, DELETE.
5. Зафиксируйте все изменения, сделайте запрос на слияние.
"""
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.projects.models import Project

class AllProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']

class ProjectDetailSerializer(ModelSerializer):
    count_of_files = serializers.IntegerField(source='files.count', read_only=True)  #
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'count_of_files']
        read_only_fields = ['created_at']  # Поля только для чтения

