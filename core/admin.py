from django.contrib import admin

from .models import Category, SubTask, Task, Project, ProjectFile, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "created_at", "due_date", "assignee")
    list_filter = ("status", "priority", "project", "created_at", "due_date", "assignee")
    search_fields = ("title",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "due_date", "created_at")
    list_filter = ("status", "task", "created_at", "due_date")
    search_fields = ("title",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "file_count")
    search_fields = ("title", "description")



@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ("file_name", "file", "created_at")
    search_fields = ("file_name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)