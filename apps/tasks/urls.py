from django.urls import path

from apps.tasks.views.tasks_views import AllTasksListAPIView
from apps.tasks.views.tag_views import TagListAPIView, TagDetailAPIView
from apps.tasks.views.tasks_views import AllTasksListAPIView, TaskDetailAPIView

app_name = 'tasks'

urlpatterns = [
    path('tasks/', AllTasksListAPIView.as_view(), name='all-tasks'),
    path('tasks/<uuid:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('tags/<uuid:pk>/', TagDetailAPIView.as_view(), name='tag-detail'),
]