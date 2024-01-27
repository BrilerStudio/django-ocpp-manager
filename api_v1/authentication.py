from rest_framework import authentication, exceptions


class ServiceAuthentication(authentication.BaseAuthentication):
    """
    Authenticate our internal service
    """

    def authenticate(self, request):
        service_token = request.META.get('HTTP_X_SERVICE_TOKEN')
        if not service_token:
            raise exceptions.AuthenticationFailed('Service Token Is Empty')

        # service_name = get_service_name(service_token)
        # if not service_name:
        #     raise exceptions.AuthenticationFailed('Service Token Invalid')
        #
        # request.service_name = service_name
