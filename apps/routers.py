from django.urls import include, path  # функции для описания маршрутов

urlpatterns = [  # общий список маршрутов API v1
    path('tasks/', include('apps.tasks.urls')),  # эндпоинты задач и тегов
    path('projects/', include('apps.projects.urls')),  # эндпоинты проектов и файлов проектов
]  # конец списка маршрутов
