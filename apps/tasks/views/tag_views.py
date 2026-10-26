from rest_framework import status  # HTTP-статусы ответов
from rest_framework.request import Request  # тип объекта запроса
from rest_framework.response import Response  # ответ DRF
from rest_framework.views import APIView  # базовый класс представления

from apps.tasks.models import Tag  # модель тега
from apps.tasks.serializers import TagSerializer  # сериализатор тега


class TagListAPIView(APIView):  # список тегов и создание нового тега
    def get_objects(self):  # получить все теги
        return Tag.objects.all()  # queryset со всеми тегами

    # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
    # Ответ 204 No Content по стандарту не должен иметь тела, а здесь передаётся data=[].
    # Пустой список — это обычный успешный результат, клиенту удобнее всегда получать 200 и массив.
    # def get(self, request: Request) -> Response:
    #     tags = self.get_objects()
    #     if not tags.exists():
    #         return Response(data=[], status=status.HTTP_204_NO_CONTENT)
    #     serializer = TagSerializer(tags, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
    def get(self, request: Request) -> Response:  # GET: список тегов
        tags = self.get_objects()  # берём все теги
        serializer = TagSerializer(tags, many=True)  # сериализуем список
        return Response(serializer.data, status=status.HTTP_200_OK)  # 200 даже для пустого списка

    # ---------- ВАРИАНТ ИЗ ПРАКТИКИ ----------
    # serializer.validated_data не содержит id созданного объекта, а return 400 недостижим:
    # при raise_exception=True невалидные данные сами дают исключение и ответ 400.
    # def post(self, request: Request) -> Response:
    #     serializer = TagSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------- УЛУЧШЕННЫЙ ВАРИАНТ ----------
    def post(self, request: Request) -> Response:  # POST: создание тега
        serializer = TagSerializer(data=request.data)  # сериализатор с входными данными
        serializer.is_valid(raise_exception=True)  # при ошибке DRF сам вернёт 400
        serializer.save()  # сохраняем тег в БД
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 и тег вместе с id
