from rest_framework import serializers

from apps.users.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'position',
            'phone',
            'last_login',
)

