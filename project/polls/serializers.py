from rest_framework import serializers
from django.contrib.auth import authenticate

from django.conf import settings
from .models import (User, Task)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=224, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        request = self.context.get('request')
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    user = serializers.SerializerMethodField()
    timestamp = serializers.CharField(read_only=True)
    content = serializers.CharField()

    class Meta:
        model = Task
        fields = ['user', 'title', 'timestamp', 'content']

    def get_user(self, obj):
        return obj.user.email

    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data.get('title', )
        content = validated_data.get('content')
        if user:
            task = Task.objects.create(user=user, title=title, content=content)
            return task
        raise serializers.ValidationError({"your task was not successful"})


