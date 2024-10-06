from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    # print(f"I am in ProjectView" 
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    # print(f"I am in queryset {queryset} serilizer_class {serializer_class} permission {permission_classes}")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.save()
        return Response({'message': 'Project deleted successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def add_user(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        project.members.add(user)
        return Response({'status': 'user added'})

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_deleted = True
        task.save()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_200_OK)