from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import EMAIL_FROM_ADDRESS
from authentication.permissions import UserObjectPermission

from .models import User
from .serializers import EmailSerializer, RegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserObjectPermission,)
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    @action(
        detail=False, url_path='me',
        methods=['get', 'patch'],
        permission_classes=(UserObjectPermission,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = RegistrationSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = self.serializer_class(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class EmailViewSet(viewsets.ModelViewSet):
    serializer_class = EmailSerializer
    permission_classes = (AllowAny, )

    @action(detail=False, url_path='email', methods=['POST'])
    def get_confirmation_code(self, request):
        confirmation_code = get_random_string(length=50)
        serializer = EmailSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            'confirmation_code',
            confirmation_code,
            EMAIL_FROM_ADDRESS,
            [request.data['email']],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='token', methods=['POST'])
    def get_auth_token_jwt(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(
                get_user_model(),
                email=email,
                confirmation_code=confirmation_code
            )
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
