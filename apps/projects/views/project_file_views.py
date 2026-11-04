from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response


from apps.projects.models import Project, ProjectFile
from apps.projects.serializers import AllProjectFilesSerializer, CreateProjectFileSerializer


class ProjectFileListGenericView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProjectFileSerializer
        return AllProjectFilesSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get('project')
        if project_name:
            return ProjectFile.objects.filter(project__title=project_name)
        return ProjectFile.objects.all()

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
