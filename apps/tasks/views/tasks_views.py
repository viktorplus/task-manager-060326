from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import Task
from apps.tasks.serializers.tasks_serializers import AllTasksSerializer, CreateTaskSerializer


class TasksPagination(PageNumberPagination):
    page_size = 5


class AllTasksListAPIView(APIView):
    pagination_class = TasksPagination

    def get_queryset(self):
        queryset = Task.objects.select_related('project', 'assignee')
        project = self.request.query_params.get('project')
        assignee = self.request.query_params.get('assignee')
        if project:
            queryset = queryset.filter(project__title=project)
        elif assignee:
            queryset = queryset.filter(assignee__email=assignee)
        return queryset

    def get(self, request: Request) -> Response:
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(self.get_queryset(), request, view=self)
        serializer = AllTasksSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)