from datetime import datetime, timedelta  # разбор дат из строки и сдвиг на сутки

from django.utils import timezone  # перевод даты в aware-datetime (USE_TZ = True)
from rest_framework import status  # HTTP-статусы ответов
from rest_framework.generics import get_object_or_404  # получить объект или вернуть 404
from rest_framework.request import Request  # тип объекта запроса
from rest_framework.response import Response  # ответ DRF
from rest_framework.views import APIView  # базовый класс представления

from apps.projects.models import Project  # модель проекта
from apps.projects.serializers import (  # сериализаторы проектов
    AllProjectsSerializer,  # список проектов
    CreateProjectSerializer,  # создание и изменение проекта
    ProjectDetailSerializer,  # подробный вид проекта
)  # конец импорта сериализаторов


class ProjectsListAPIView(APIView):  # список проектов с фильтром по датам и создание проекта
    # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
    # Фильтрует только когда переданы обе даты, условие "if date_from else ..." внутри уже
    # проверенного блока бессмысленно, date_to не включает сам день (берётся 00:00),
    # а кривая дата вызывает ValueError прямо в запросе -> 500.
    # def get_objects(self, date_from=None, date_to=None):
    #     if date_from and date_to:
    #         date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
    #         date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None
    #         return Project.objects.filter(created_at__range=(date_from, date_to))
    #     return Project.objects.all()

    # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
    def get_objects(self, date_from=None, date_to=None):  # проекты с необязательным фильтром по датам
        projects = Project.objects.all()  # по умолчанию все проекты
        if date_from:  # передана начальная дата
            start = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))  # начало дня date_from
            projects = projects.filter(created_at__gte=start)  # создано не раньше date_from
        if date_to:  # передана конечная дата
            end = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d')) + timedelta(days=1)  # начало следующего дня
            projects = projects.filter(created_at__lt=end)  # создано не позже конца дня date_to
        return projects  # итоговый queryset

    def get(self, request: Request) -> Response:  # GET: список проектов
        date_from = request.query_params.get('date_from')  # ?date_from=YYYY-MM-DD
        date_to = request.query_params.get('date_to')  # ?date_to=YYYY-MM-DD
        try:  # неверный формат даты даёт ValueError в strptime
            projects = self.get_objects(date_from, date_to)  # проекты с фильтром
        except ValueError:  # дата не в формате YYYY-MM-DD
            return Response({"error": "Dates must be in format YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)  # 400 вместо 500
        serializer = AllProjectsSerializer(projects, many=True)  # сериализуем список
        return Response(serializer.data, status=status.HTTP_200_OK)  # 200 и список проектов

    def post(self, request: Request) -> Response:  # POST: создание проекта
        serializer = CreateProjectSerializer(data=request.data)  # сериализатор с входными данными
        serializer.is_valid(raise_exception=True)  # при ошибке DRF вернёт 400
        serializer.save()  # сохраняем проект в БД
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 и созданный проект


class ProjectDetailAPIView(APIView):  # один проект: просмотр, частичное изменение, удаление
    def get_object(self, pk):  # найти проект по UUID
        return get_object_or_404(Project, pk=pk)  # 404, если проекта нет

    def get(self, request: Request, pk) -> Response:  # GET: один проект
        project = self.get_object(pk)  # проект или 404
        serializer = ProjectDetailSerializer(project)  # подробный сериализатор с file_count
        return Response(serializer.data, status=status.HTTP_200_OK)  # 200 и данные проекта

    def put(self, request: Request, pk) -> Response:  # PUT: частичное обновление проекта
        project = self.get_object(pk)  # проект или 404
        serializer = CreateProjectSerializer(instance=project, data=request.data, partial=True)  # можно передать только часть полей
        serializer.is_valid(raise_exception=True)  # при ошибке DRF вернёт 400
        serializer.save()  # сохраняем изменения
        return Response(serializer.data, status=status.HTTP_200_OK)  # 200 и обновлённый проект

    def delete(self, request: Request, pk) -> Response:  # DELETE: удаление проекта
        project = self.get_object(pk)  # проект или 404
        project.delete()  # удаляем проект (его задачи удалятся каскадно)
        return Response({"message": "Project was deleted successfully"}, status=status.HTTP_200_OK)  # 200 и сообщение
