from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import get_object_or_404
from apps.tasks.models import Task
from apps.tasks.serializers.tasks_serializers import (
    AllTasksSerializer,
    CreateUpdateTaskSerializer,
    TaskDetailSerializer,
)


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
        serializer = CreateUpdateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self, request: Request, pk) -> Response:
        task = self.get_object(pk)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        return self._update(request, pk, partial=False)

    def patch(self, request: Request, pk) -> Response:
        return self._update(request, pk, partial=True)

    def _update(self, request: Request, pk, partial: bool) -> Response:
        task = self.get_object(pk)
        serializer = CreateUpdateTaskSerializer(instance=task, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TaskDetailSerializer(task).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        task = self.get_object(pk)
        task.delete()
        return Response({'message': 'The task has been deleted.'}, status=status.HTTP_200_OK)