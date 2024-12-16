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
    dependencies = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), many=True, required=False
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title', 'description', 'status', 'priority',
            'due_date', 'is_deleted', 'dependencies', 'assigned_to'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)


    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'members', 'tasks', 'is_deleted']

    def create(self, validated_data):
        
        members = validated_data.pop('members', [])
        project = Project.objects.create(**validated_data)
        project.members.set(members)

        return project
