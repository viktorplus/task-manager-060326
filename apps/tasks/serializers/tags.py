from rest_framework.serializers import ModelSerializer
from apps.tasks.models import Tag, Task

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

        """Задание 20
1. Напишите сериализатор TaskInfoSerializer для получения подробной информации о задаче.
2. Поле для тегов должно быть вложенным объектом, которым является уже готовый сериализатор
TagsSerializer"""

class TaskInfoSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'tags']