from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField, SerializerMethodField

from .models import (
    UserAccounts
)


class RefreshTokenSerialzierPost(Serializer):
    refresh = CharField()


class UserSerialzier(ModelSerializer):
    class Meta:
        model = UserAccounts
        fields = ['id', 'first_name', 'last_name', 'patronymic_name',
                  'phone', 'email', 'avatar', 'birthday']


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserAccounts
        fields = UserSerialzier.Meta.fields
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'patronymic_name': {'required': False},
            'birthday': {'required': False},
            'email': {'required': False},
            'avatar': {'required': False},
            'phone': {'required': False}
        }


class LoginSerializer(Serializer):
    phone = CharField()
    password = CharField()


class RegisterSeialzier(Serializer):
    first_name = CharField()
    last_name = CharField()
    patronymic_name = CharField()
    birthday = CharField()
    email = CharField()
    phone = CharField()
    password = CharField()