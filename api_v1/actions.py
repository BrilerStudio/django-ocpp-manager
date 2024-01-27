from rest_framework.response import Response


def detail_action(view):
    """
    Perform detail action with custom serializer
    :param view:
    :return:
    """

    instance = view.get_object()
    serializer = view.get_serializer(instance, data=view.request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
