from rest_framework import serializers


class EnumSerializer(serializers.Serializer):
    id = serializers.CharField(
        read_only=True,
        allow_null=True,
    )

    value = serializers.CharField(
        read_only=True,
        allow_null=True,
    )
    name = serializers.CharField(
        read_only=True,
        allow_null=True,
    )
