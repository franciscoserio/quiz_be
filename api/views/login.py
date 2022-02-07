from api.serializers.user_serializers import LoginSerializer


def jwt_response_payload_handler(token, email=None, request=None):

    return {
        "token": token,
        "user": LoginSerializer(email, context={"request": request}).data,
    }
