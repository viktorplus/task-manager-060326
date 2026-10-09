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

# task1 = Task.objects.create(
#     title="Backend Task 2",
#     description="This is a backend task.",
#     status=Task.Status.NEW,
#     priority=Task.Priority.HIGH,
#     project=Project.objects.get(title="Project1"),
#     due_date=date(2024, 6, 30),
#     assignee=User.objects.get(username="Backend"),
# )
#
# task2 = Task.objects.create(
#     title="Frontend Task 2",
#     description="This is a frontend task.",
#     #categories= Category.objects.get(name="Category1"),
#     status=Task.Status.NEW,
#     priority=Task.Priority.MEDIUM,
#     project=Project.objects.get(title="Project1"),
#     due_date=date(2024, 7, 15),
#     assignee=User.objects.get(username="Frontend")
# )

# task3 = Task.objects.create(
#     title="DevOps Task 2",
#     description="This is a DevOps task.",
#     status=Task.Status.NEW,
#     priority=Task.Priority.LOW,
#     project=Project.objects.get(title="Project2"),
#     due_date=timezone.make_aware(datetime(2024, 6, 30)),
#     assignee=User.objects.get(username="DevOPS")
# )

"""Задание 6
1. Получите все объекты тегов.
2. У каждого объекта созданных задач обратитесь к полю тегов через точку.
3. У поля ManyToMany (tags) вызовите метод add и передайте ему объект тега.
○ Объект тега будет зависеть от того, какой title будет в задаче, например:
(‘Добавить новый эндпоинтʼ - Backend tag, ‘Обновить страницу ответа 404ʼ - Frontend tag)"""

# task1 = Task.objects.get(title="Backend Task 2")
# backend_tag = Tag.objects.get(name="Backend")
# task1.tag.add(backend_tag)

###tiger_task_1.tags.add(back_tag)

# task2 = Task.objects.get(title="Frontend Task 2")
# frontend_tag = Tag.objects.get(name="Frontend")
# task2.tag.add(frontend_tag)
#
# task3 = Task.objects.get(title="Backend Task 1")
# backend_tag = Tag.objects.get(name="Backend")
# task3.tag.add(backend_tag)

"""Задание 7
1. Импортируйте модели тегов Tag.
2. Напишите запрос, который позволит получить список всех тегов.
3. Выведите имя каждого тега.
4. Получите самый первый тег.
5. Получите самый последний тег.
6. Получите кол-во всех тегов.
"""


# all_tags = Tag.objects.all()
# for tag in all_tags:
#     print(tag.name)
#
# first_tag = Tag.objects.first()
# print("Первый тег:", first_tag.name)
#
# last_tag = Tag.objects.last()
# print("Последний тег:", last_tag.name)
#
# tags_count = Tag.objects.count()
# print("Количество тегов:", tags_count)

