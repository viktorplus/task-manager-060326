from django.urls import path

from apps.projects.views.project_views import ProjectsListAPIView, ProjectDetailAPIView
from apps.projects.views.project_file_views import (
    ProjectFileListGenericView,
    ProjectFileDetailGenericView,
    DowloadProjectFileView,
)

app_name = 'projects'

urlpatterns = [
    path('', ProjectsListAPIView.as_view(), name='project-list'),
    path('files/', ProjectFileListGenericView.as_view(), name='project-file-list'),
    path('files/<uuid:pk>/', ProjectFileDetailGenericView.as_view(), name='project-file-detail'),
    path('<uuid:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('files/donload/<uuid:pk>/', DowloadProjectFileView.as_view(), name='donload-project-file'),
]