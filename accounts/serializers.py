from django.contrib.auth import get_user_model
from rest_framework import serializers
import jwt

User = get_user_model()

jwt_secret = 'THE_SECRET_OF_THE_UNIVERSE'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'bio')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
