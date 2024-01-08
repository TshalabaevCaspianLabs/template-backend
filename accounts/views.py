from django.contrib.auth.models import update_last_login

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from utils import BaseCRUD, CustomPagination
from .models import (
    UserAccounts
)
from .serializer import (
    LoginSerializer, RegisterSeialzier, UserSerialzier, RefreshTokenSerialzierPost, UserUpdateSerializer
)


class UserBaseViewSet(BaseCRUD):
    permission_classes = [AllowAny]
    serializer_class = UserSerialzier
    pagination_class = CustomPagination

    _model = UserAccounts
    _serializer = serializer_class
    _serializer_update = UserUpdateSerializer

    @swagger_auto_schema(
        request_body=RegisterSeialzier,
        responses={200: UserSerialzier, 400: 'Bad Request'},
        operation_summary="Create New User Account",
        operation_description="This endpoint created new user account.",
        tags=["AUTH"]
    )
    def create(self, request):
        serializer = RegisterSeialzier(data=request.data)
        if serializer.is_valid():
            user = UserAccounts.objects.create_user(
                phone=serializer.data['phone'],
                password=serializer.data['password']
            )

            user.first_name = serializer.data['first_name']
            user.last_name = serializer.data['last_name']
            user.patronymic_name = serializer.data['patronymic_name']
            user.birthday = serializer.data['birthday']
            user.email = serializer.data['email']
            user.is_active = True
            user.is_confirmed = True
            user.in_consideration = True
            user.save()

            serialzier = self._serializer(user)
            return Response(serialzier.data, 200)
        else:
            return Response(serializer.errors, 400)

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: UserSerialzier, 400: 'Bad Request'},
        operation_summary="Create New User Account",
        operation_description="This endpoint created new user account.",
        tags=["AUTH"]
    )
    def login(self, request):
        serialzier = LoginSerializer(data=request.data)
        if serialzier.is_valid():
            try:
                user = UserAccounts.objects.get(phone=serialzier.data['phone'])
            except:
                return Response({"message": 'This user not found in system'}, 400)

            refresh = RefreshToken.for_user(user)
            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'in_moderation': user.in_consideration,
                'id_user': user.id,
            }
            update_last_login(None, user)
            return Response(data, 200)
        else:
            return Response(serialzier.errors, 400)

    @swagger_auto_schema(
        responses={200: UserSerialzier, 400: 'Bad Request'},
        operation_summary="Get info User Account",
        operation_description="This endpoint geting info user account.",
        tags=["User"]
    )
    def me(self, request):
        try:
            user = UserAccounts.objects.get(id=request.user.id)
        except:
            return Response({"message": "This user not found system"}, 404)

        serialzier = UserSerialzier(user)
        return Response(serialzier.data)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserSerialzier, 400: 'Bad Request'},
        operation_summary="Update data User Account",
        operation_description="This endpoint updated user account.",
        tags=["User"]
    )
    def update(self, request, id):
        if request.user.id == id:
            return super().update(request, id)
        else:
            return Response({"message": 'User is not authorized'}, 403)
        

class RefreshViewSet(GenericViewSet):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        request_body=RefreshTokenSerialzierPost,
        responses={200: TokenRefreshSerializer, 400: 'Bad Request'},
        operation_summary="Refresh JWT Token",
        operation_description="This endpoint refresh JWT token.",
        tags=["AUTH"]
    )
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, 200)
        else:
            return Response(serializer.errors, 400)
