from django.db import models
from .base import TimeStampedModel, UUIDv7Model

"""Задача 1
Создайте модель Project со следующими полями:
• Название проекта: строковое, уникальное
• Описание проекта: строковое, большое поле, обязательно к заполнению
• Дата создания проекта: должна проставляться автоматически при создании
"""

class Project(UUIDv7Model, TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "task_manager_project"
        ordering = ["-title"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "description"],
                name="unique_project_title_description",
            ),
        ]

    def __str__(self):
        return self.title

