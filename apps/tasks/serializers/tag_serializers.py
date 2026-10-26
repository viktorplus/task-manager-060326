from rest_framework.serializers import ModelSerializer  # базовый сериализатор для моделей
from apps.tasks.models import Tag  # модель тега


class TagSerializer(ModelSerializer):  # сериализатор тега
    class Meta:  # настройки сериализатора
        model = Tag  # сериализуем модель Tag
        fields = '__all__'  # все поля модели: id и name
