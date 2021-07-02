from django.conf import settings


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token
    }
