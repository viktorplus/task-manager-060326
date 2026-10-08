import os
from datetime import date

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Tag, Project, ProjectFile

# new_tag = Tag.objects.create(name="Backend")
# new_tag = Tag.objects.create(name="Frontend")
# new_tag = Tag.objects.create(name="Q&A")
# new_tag = Tag.objects.create(name="Design")
# new_tag = Tag.objects.create(name="Devops")


new_project1 = Project.objects.create(title="Project_1", description="This is my first project.")

project2 = Project(title = "Project_2", description = "This is my second project.")
project2.save()

proj1_file = ProjectFile.objects.create(file_name="file1.txt", file="projects/1/file.txt")
proj2_file = ProjectFile.objects.create(file_name="file2.txt", file="projects/2/file.txt")

new_project1.files.add(proj1_file)
project2.files.add(proj2_file)



