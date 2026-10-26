
"""Задание 10
1. Установите модуль djangorestframework.
2. Добавить этот модуль в файл requirements.txt.
3. Добавить этот модуль в список установленных приложений в файле settings.py.
4. Создать новый пакет serializers, в котором создать первый файл - projects
5. Импортируйте класс ModelSerializer.
6. Напишите первый сериализатор, который будет обрабатывать поля id и name для проекта,
выдавая общую базу для вывода всех проектов.
"""
from rest_framework import serializers  # поля и ошибки валидации DRF
from rest_framework.serializers import ModelSerializer  # базовый сериализатор для моделей

from apps.projects.models import Project  # модель проекта


class AllProjectsSerializer(ModelSerializer):  # краткий вид проекта для списка
    class Meta:  # настройки сериализатора
        model = Project  # сериализуем модель Project
        # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
        # В модели нет поля name, название проекта хранится в title.
        # fields = ('id', 'name', 'created_at')
        # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
        fields = ('id', 'title', 'created_at')  # id, название и дата создания


class CreateProjectSerializer(ModelSerializer):  # создание и изменение проекта
    created_at = serializers.DateTimeField(read_only=True)  # дату ставит БД, клиент её не передаёт

    class Meta:  # настройки сериализатора
        model = Project  # сериализуем модель Project
        # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
        # В модели нет поля name, название проекта хранится в title.
        # fields = ('name', 'description', 'created_at')
        # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
        fields = ('title', 'description', 'created_at')  # поля для создания проекта

    def validate_description(self, value: str) -> str:  # проверка описания
        if len(value) < 30:  # описание слишком короткое
            raise serializers.ValidationError("Description must be at least 30 characters long")  # ошибка 400
        return value  # описание прошло проверку
