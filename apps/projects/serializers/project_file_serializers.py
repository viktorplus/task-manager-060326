from rest_framework import serializers  # ошибки валидации DRF
from rest_framework.serializers import ModelSerializer  # базовый сериализатор для моделей

from apps.projects.models import ProjectFile  # модель файла проекта
# ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
# Опечатка в имени модуля (upload_file_helper без "s") -> ModuleNotFoundError.
# from apps.projects.utils.upload_file_helper import ...
# ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
from apps.projects.utils.upload_file_helpers import (  # функции и константы для загрузки файлов
    ALLOWED_EXTENSIONS,  # разрешённые расширения
    MAX_FILE_SIZE_MB,  # максимальный размер в МБ
    check_extension,  # проверка расширения
    check_file_size,  # проверка размера
    create_file_path,  # построение пути файла
    save_file,  # запись файла на диск
)  # конец импорта помощников


class AllProjectFilesSerializer(ModelSerializer):  # список файлов проектов
    class Meta:  # настройки сериализатора
        model = ProjectFile  # сериализуем модель ProjectFile
        # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
        # Поля 'project' нет: связь идёт из Project.files с related_name="projects".
        # fields = ('id', 'file_name', 'project')
        # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
        fields = ('id', 'file_name', 'projects')  # projects — список UUID проектов, к которым привязан файл


class CreateProjectFileSerializer(ModelSerializer):  # создание файла проекта
    class Meta:  # настройки сериализатора
        model = ProjectFile  # сериализуем модель ProjectFile
        fields = ('file_name',)  # клиент передаёт только имя файла

    def validate_file_name(self, value: str) -> str:  # проверка имени файла
        if not value.isascii():  # в имени есть не-ASCII символы
            raise serializers.ValidationError("Please, provide a valid file name.")  # ошибка 400
        if not check_extension(value):  # расширение не из разрешённых
            raise serializers.ValidationError(f"Valid file extensions: {ALLOWED_EXTENSIONS}")  # ошибка 400
        return value  # имя прошло проверку

    def create(self, validated_data):  # сохранение файла и записи в БД
        raw_file = self.context.get('raw_file')  # загруженный файл передаётся через context
        if not check_file_size(raw_file):  # файл больше лимита
            raise serializers.ValidationError(f"File size is too large ({MAX_FILE_SIZE_MB} MB as maximum).")  # ошибка 400
        file_path = create_file_path(validated_data['file_name'])  # путь внутри MEDIA_ROOT
        save_file(file_path, raw_file)  # записываем файл на диск
        # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
        # Поля file_path в модели нет, FileField называется file.
        # validated_data['file_path'] = file_path
        # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
        validated_data['file'] = file_path  # путь сохраняется в FileField модели
        return ProjectFile.objects.create(**validated_data)  # создаём запись о файле
