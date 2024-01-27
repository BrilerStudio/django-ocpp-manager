from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'is_superuser',
            'last_name',
            'username',
        ]

        read_only_fields = [
            'id',
            'email',
            'first_name',
            'is_superuser',
            'last_name',
            'username',
        ]

        ref_name = None
