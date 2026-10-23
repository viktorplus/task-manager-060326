from django.contrib import admin
from .models import Project, ProjectFile
from django.contrib import admin, messages
from django.utils import timezone

from apps.core.admin import replace_spaces_with_underscores


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "file_count")
    search_fields = ("title", "description")
    actions = [replace_spaces_with_underscores]




@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ("file_name", "file", "created_at")
    search_fields = ("file_name",)
    actions = [replace_spaces_with_underscores]
