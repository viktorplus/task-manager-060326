from django.urls import path

from apps.projects.views.project_views import ProjectsListAPIView, ProjectDetailAPIView
from apps.projects.views.project_file_views import ProjectFileListGenericView

app_name = 'projects'




urlpatterns = [
    path('', ProjectsListAPIView.as_view(), name='project-list'),
    path('files/', ProjectFileListGenericView.as_view(), name='project-file-list'),
    path('<uuid:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),

]
