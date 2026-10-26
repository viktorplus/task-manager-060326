from rest_framework.serializers import ModelSerializer
from apps.tasks.models import Task
from .tags import TagSerializer


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority']


class TaskInfoSerializer(ModelSerializer):
    tag = TagSerializer( many=True) # source='tag' - если поле в модели называется иначе, то указываем source='имя_поля_в_модели'
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'tag', 'project', 'created_at', 'updated_at', 'due_date']