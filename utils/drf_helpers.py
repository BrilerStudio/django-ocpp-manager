from rest_framework.response import Response


def create_handler(self, request, context: dict = None, *args, **kwargs):
    if not context:
        context = self.get_serializer_context()

    serializer = self.get_serializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def update_handler(self, request, *args, **kwargs):
    serializer = self.get_serializer(self.get_object(), data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def delete_handler(self, request, *args, **kwargs):
    instance = self.get_object()
    instance.delete()
    return Response(status=204)
