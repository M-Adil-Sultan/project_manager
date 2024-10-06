from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Task

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'status', 'due_date', 'is_deleted']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    print(f"I am in serializer")
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)


    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'members', 'tasks', 'is_deleted']

    def create(self, validated_data):
        print(f"I am in create")
        
        members = validated_data.pop('members', [])
        project = Project.objects.create(**validated_data)
        project.members.set(members)

        return project
