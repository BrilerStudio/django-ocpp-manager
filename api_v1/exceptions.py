import logging
from enum import Enum

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.utils.log import log_response
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    is_client_error,
    is_server_error,
)
from rest_framework.views import set_rollback


class ErrorType(str, Enum):
    AUTH_ERROR = 'authentication_error'
    CLIENT_ERROR = 'client_error'
    VALIDATION_ERROR = 'validation_error'
    SERVER_ERROR = 'server_error'


def api_exception_handler(exc, context):
    logging.exception(
        exc,
        extra={
            'context_str': str(context),
        },
    )

    # convert well-known Django exceptions
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    elif isinstance(exc, ValidationError):
        exc = exceptions.APIException(
            {
                'code': exc.code,
                'detail': exc.message,
                # 'data': exc.params,
            },
        )

    set_rollback()

    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        data = {
            'type': ErrorType.AUTH_ERROR,
            'errors': [
                {
                    'code': exc.detail.code,
                    'detail': str(exc.detail),
                },
            ],
        }
        response = Response(data, status=HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, exceptions.APIException):
        headers = {}
        wait = getattr(exc, 'wait', None)
        if wait:
            headers['Retry-After'] = str(wait)

        if isinstance(exc, exceptions.ValidationError):
            error_type = ErrorType.VALIDATION_ERROR
        elif is_client_error(exc.status_code):
            error_type = ErrorType.CLIENT_ERROR
        else:
            error_type = ErrorType.SERVER_ERROR

        data = {
            'type': error_type,
            'errors': flatten_errors(exc.detail),
        }

        response = Response(data, status=exc.status_code, headers=headers)
    else:
        data = {
            'type': ErrorType.SERVER_ERROR,
            'errors': [
                {
                    'code': 'internal',
                    'detail': 'Internal error',
                },
            ],
        }
        response = Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)

    if is_server_error(response.status_code):
        request = getattr(context['request'], '_request', None)

        log_response(
            '%s: %s',
            getattr(exc, 'detail', exc),
            getattr(request, 'path', ''),
            response=response,
            request=request,
            exception=exc,
        )

    return response


def flatten_errors(detail: (list, dict, exceptions.ErrorDetail), attr=None, index=None) -> [dict]:
    if not detail:
        return []
    elif isinstance(detail, list):
        first_item, *rest = detail
        if not isinstance(first_item, exceptions.ErrorDetail):
            index = 0 if index is None else index + 1
            new_attr = f'{attr}.{index}' if attr else str(index)
            return flatten_errors(first_item, new_attr, index) + flatten_errors(rest, attr, index)
        else:
            return flatten_errors(first_item, attr, index) + flatten_errors(rest, attr, index)
    elif isinstance(detail, dict):
        (key, value), *rest = list(detail.items())
        if attr:
            key = f'{attr}.{key}'
        return flatten_errors(value, key) + flatten_errors(dict(rest), attr)
    else:
        return [
            {
                'code': detail.code,
                'detail': str(detail),
                'attr': attr,
            },
        ]
