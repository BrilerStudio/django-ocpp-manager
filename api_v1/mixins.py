from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from api_v1.exceptions import ErrorType, api_exception_handler
from api_v1.paginations import AdminPageNumberPagination


class ApiV1ViewMixin:
    tags = [
        'ApiV1',
    ]
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    pagination_class = AdminPageNumberPagination

    # noinspection PyMethodMayBeStatic
    def get_exception_handler(self):
        return api_exception_handler


def api_v1_page_not_found(request, exception, **kwargs):
    return JsonResponse(
        data={
            'type': ErrorType.CLIENT_ERROR,
            'errors': [
                {
                    'code': 'not_found',
                    'detail': 'Not Found',
                },
            ],
        },
        status=404,
    )
