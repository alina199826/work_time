from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import VerificationToken
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'last_name', 'organization', 'login', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        user = User.objects.create(password=password, **validated_data)
        return user


class VerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationToken
        fields = ('token',)
        extra_kwargs = {
            'token': {'read_only': True}
        }

    def create(self, validated_data):
        token = get_random_string(length=32)
        user = self.context['request'].user
        verification_token = VerificationToken.objects.create(user=user, token=token)
        return verification_token