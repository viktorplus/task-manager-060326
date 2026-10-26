from rest_framework import status  # HTTP-статусы ответов
from rest_framework.generics import get_object_or_404  # получить объект или вернуть 404
from rest_framework.request import Request  # тип объекта запроса
from rest_framework.response import Response  # ответ DRF
from rest_framework.views import APIView  # базовый класс представления

from apps.projects.models import Project, ProjectFile  # модели проекта и файла проекта
from apps.projects.serializers import AllProjectFilesSerializer, CreateProjectFileSerializer  # сериализаторы файлов


class ProjectFileListAPIView(APIView):  # список файлов проектов и загрузка нового файла
    def get_objects(self, project_name=None):  # файлы, при необходимости только одного проекта
        if project_name:  # передано название проекта
            return ProjectFile.objects.filter(projects__title=project_name)  # файлы проекта с таким title
        return ProjectFile.objects.all()  # иначе все файлы

    def get(self, request: Request) -> Response:  # GET: список файлов
        project_name = request.query_params.get('project')  # ?project=<title>
        files = self.get_objects(project_name)  # файлы с фильтром
        serializer = AllProjectFilesSerializer(files, many=True)  # сериализуем список
        return Response(serializer.data, status=status.HTTP_200_OK)  # 200 и список файлов

    # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
    # request.FILES["file"] без файла даёт KeyError -> 500, а успешная загрузка возвращает 200 вместо 201.
    # def post(self, request: Request) -> Response:
    #     file = request.FILES["file"]
    #     project_id = request.data.get("project_id")
    #     project = get_object_or_404(Project, pk=project_id)
    #     serializer = CreateProjectFileSerializer(data=request.data, context={"raw_file": file})
    #     if serializer.is_valid(raise_exception=True):
    #         project_file = serializer.save()
    #         project_file.projects.set([project])
    #         return Response({"message": "File upload successfully"}, status=status.HTTP_200_OK)

    # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
    def post(self, request: Request) -> Response:  # POST: загрузка файла (multipart/form-data)
        file = request.FILES.get('file')  # загруженный файл или None
        project_id = request.data.get('project_id')  # UUID проекта
        if not file or not project_id:  # не хватает обязательных полей
            return Response({"error": "Fields 'file' and 'project_id' are required."}, status=status.HTTP_400_BAD_REQUEST)  # 400 вместо 500
        project = get_object_or_404(Project, pk=project_id)  # проект или 404 (невалидный UUID DRF тоже превращает в 404)
        serializer = CreateProjectFileSerializer(data=request.data, context={"raw_file": file})  # имя файла + сам файл в context
        serializer.is_valid(raise_exception=True)  # при ошибке DRF вернёт 400
        project_file = serializer.save()  # проверка размера, запись на диск и в БД
        project_file.projects.set([project])  # привязываем файл к проекту
        return Response({"message": "File upload successfully"}, status=status.HTTP_201_CREATED)  # 201 — файл создан
