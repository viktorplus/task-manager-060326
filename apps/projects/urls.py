from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import get_all_projects, ProjectDetailAPIView

app_name = 'projects'

urlpatterns = [
    path('', get_all_projects, name='get_all_projects'),
    path('<uuid:pk>/', ProjectDetailAPIView.as_view(), name='project_detail'),
]
