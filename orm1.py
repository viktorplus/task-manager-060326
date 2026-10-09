import os
from datetime import date
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Tag, Project, ProjectFile

# 1 Создание тэгов для будущих задач

# new_tag = Tag.objects.create(name="Backend")
# new_tag = Tag.objects.create(name="Frontend")
# new_tag = Tag.objects.create(name="Q&A")
# new_tag = Tag.objects.create(name="Design")
# new_tag = Tag.objects.create(name="Devops")

# 2 Создание проектов и файлов для них
# new_project1 = Project.objects.create(title="Project_1", description="This is my first project.")
#
# project2 = Project(title = "Project_2", description = "This is my second project.")
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

# user = User.objects.filter(username="Designer").first()

users = User.objects.filter(
    username__in=["Backend", "Frontend", "DevOPS", "Q&A", "Designer"]
)
# пролверка, что все пользователи созданы
print(list(users.values("id", "username")))
print("Количество:", users.count())

