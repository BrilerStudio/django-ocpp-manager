from rest_framework import serializers


class CustomSlugRelatedField(serializers.SlugRelatedField):
    """
    Extended SlugRelatedField to accept a serializer_class for swagger documentation.
    """

    def __init__(
            self,
            serializer_class: type(serializers.Serializer),
            slug_field: str = 'code',
            max_length: str = None,
            *args,
            **kwargs,
    ):
        self._serializer_class = serializer_class
        self.max_length = max_length
        super().__init__(slug_field, **kwargs)

    def to_representation(self, value):
        if self._serializer_class:
            return self._serializer_class(value).data
        return super().to_representation(value)
