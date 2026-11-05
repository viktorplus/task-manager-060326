from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.projects.models import Project
from apps.projects.serializers import AllProjectsSerializer
from apps.projects.serializers.projects import ProjectDetailSerializer


@api_view(['GET'])
def get_all_projects(request: Request):
    projects = Project.objects.all()
    serializer = AllProjectsSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, pk) -> Response:
        return self.put(request, pk)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response({'message': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
