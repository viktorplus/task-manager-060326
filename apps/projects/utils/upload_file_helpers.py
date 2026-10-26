import os  # работа с путями и папками
from pathlib import Path  # разбор имени файла

from django.conf import settings  # MEDIA_ROOT из настроек проекта

# ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
# '.py' в списке разрешённых позволяет загружать исполняемый код — лишнее расширение.
# ALLOWED_EXTENSIONS = ['.pdf', '.csv', '.doc', '.xlsx', '.py']
# ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
ALLOWED_EXTENSIONS = ['.pdf', '.csv', '.doc', '.xlsx']  # разрешённые расширения файлов
MAX_FILE_SIZE_MB = 2  # максимальный размер файла в мегабайтах


def check_extension(filename: str) -> bool:  # проверка расширения файла
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS  # последнее расширение без учёта регистра


def check_file_size(file, required_size: int = MAX_FILE_SIZE_MB) -> bool:  # проверка размера файла
    return file.size <= required_size * 1024 * 1024  # размер в байтах не больше лимита


# ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
# Папка 'documents/' не совпадает с upload_to="projects/" модели, split('.') ломается на "a.b.pdf",
# а имя вида "../x.pdf" позволяет выйти из папки media.
# def create_file_path(file_name):
#     name, extension = file_name.split('.')
#     return f"documents/{name}.{extension}"
# ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
def create_file_path(file_name: str) -> str:  # относительный путь файла внутри MEDIA_ROOT
    return f"projects/{Path(file_name).name}"  # только имя файла (без "../" и папок), папка как в upload_to модели


def save_file(file_path: str, file_content) -> str:  # сохранить загруженный файл на диск
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)  # абсолютный путь внутри MEDIA_ROOT
    os.makedirs(os.path.dirname(full_path), exist_ok=True)  # создаём папку, если её ещё нет
    with open(full_path, 'wb') as destination:  # открываем файл на запись в бинарном режиме
        for chunk in file_content.chunks():  # читаем загруженный файл частями, не целиком в память
            destination.write(chunk)  # записываем очередную часть
    return file_path  # относительный путь для сохранения в модели
