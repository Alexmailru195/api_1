from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        """
        Проверка совпадения паролей.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        """
        Создание пользователя.
        """
        validated_data.pop('password2')  # Удаляем password2 из данных
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """
        Обновление данных пользователя.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Обновляем пароль, если он предоставлен
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
