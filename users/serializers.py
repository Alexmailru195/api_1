from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .validators import ContainsLetterValidator
from django.core.exceptions import ValidationError


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'birth_date', 'profile_picture', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}},
            'email': {'required': True},
        }

    def validate_password(self, password):
        validator = ContainsLetterValidator()
        try:
            validator.validate(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        if len(password) < 8:
            raise serializers.ValidationError("Пароль должен быть не менее 8 символов.")
        return password

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)