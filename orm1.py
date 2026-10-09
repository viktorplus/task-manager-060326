import os
from datetime import date, datetime
from django.utils import timezone

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Tag, Project, ProjectFile, Task, Category

# 1 Создание тэгов для будущих задач

# new_tag = Tag.objects.create(name="Backend")
# new_tag = Tag.objects.create(name="Frontend")
# new_tag = Tag.objects.create(name="Q&A")
# new_tag = Tag.objects.create(name="Design")
# new_tag = Tag.objects.create(name="Devops")

# 2 Создание проектов и файлов для них
# new_project1 = Project.objects.create(title="Project1", description="This is my first project.")
#
# project2 = Project(title = "Project2", description = "This is my second project.")
# project2.save()
#
# proj1_file = ProjectFile.objects.create(file_name="file1.txt", file="projects/1/file.txt")
# proj2_file = ProjectFile.objects.create(file_name="file2.txt", file="projects/2/file.txt")
#
# new_project1.files.add(proj1_file)
# project2.files.add(proj2_file)

# 3 Создание пользователей для работы в проекте.
# Импортируйте модель Пользователя (User), которого по умолчанию предлагает Django.

# backend_user = User.objects.create(username="Backend", password="password")
# frontend_user = User.objects.create(username="Frontend", password="password")
# devops_user = User.objects.create(username="DevOPS", password="password")
# qa_user = User.objects.create(username="Q&A", password="password")
# designer_user = User.objects.create(username="Designer", password="password")


# пролверка, что все пользователи созданы
# user = User.objects.filter(username="Designer").first()

# users = User.objects.filter(
#     username__in=["Backend", "Frontend", "DevOPS", "Q&A", "Designer"]
# )
#
# print(list(users.values("id", "username")))
# print("Количество:", users.count())

"""Задание 5
1. Импортируйте модель Task.
2. Для каждого проекта создайте задачи. По одной-две для каждого тега.
3. Для foreignkey полей передаём объекты, которые мы создавали ранее.
4. Убедитесь, что данные были созданы и сохранены в базу данных.
"""

task1 = Task.objects.create(
    title="Backend Task 2",
    description="This is a backend task.",
    status=Task.Status.NEW,
    priority=Task.Priority.HIGH,
    project=Project.objects.get(title="Project1"),
    due_date=date(2024, 6, 30),
    assignee=User.objects.get(username="Backend"),
)

task2 = Task.objects.create(
    title="Frontend Task 2",
    description="This is a frontend task.",
    #categories= Category.objects.get(name="Category1"),
    status=Task.Status.NEW,
    priority=Task.Priority.MEDIUM,
    project=Project.objects.get(title="Project1"),
    due_date=date(2024, 7, 15),
    assignee=User.objects.get(username="Frontend")
)


