from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response


from apps.projects.models import Project, ProjectFile
from apps.projects.serializers import AllProjectFilesSerializer, CreateProjectFileSerializer, ProjectFileDetailSerializer


class ProjectFileListGenericView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AllProjectFilesSerializer
        return CreateProjectFileSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get('project')

        if project_name:
            project_file = ProjectFile.objects.filter(
                projects__title=project_name
            )
            return project_file

        return ProjectFile.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        project_files = self.get_queryset()

        if not project_files.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.get_serializer(project_files, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request: Request, *args, **kwargs):
        file = request.FILES.get('file')
        project_id = request.data.get('project_id')
        if not file or not project_id:
            return Response(
                {"error": "Fields 'file' and 'project_id' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        project = get_object_or_404(Project, pk=project_id)

        serializer = self.get_serializer(data={'file_name': file.name})
        serializer.context.update({'project': project, 'raw_file': file})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "File uploaded successfully."}, status=status.HTTP_201_CREATED)

class ProjectFileDetailGenericView(RetrieveDestroyAPIView):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileDetailSerializer

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        project_file = self.get_object()
        project_file.file.delete(save=False)  # удаляем файл с диска
        project_file.projects.clear()         # удаляем связь с проектами
        project_file.delete()                 # удаляем запись из БД
        return Response({"message": "File deleted successfully"}, status=status.HTTP_200_OK)