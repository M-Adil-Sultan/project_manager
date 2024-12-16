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
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

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

    def perform_create(self, serializer):
        task = serializer.save()
        if task.assigned_to:
            self.send_assignment_email(task)
    
    def send_assignment_email(self, task):
        subject = f'Task Assignment: {task.title}'
        message = f'You have been assigned to the task "{task.title}" in project "{task.project.name}".'
        recipient = task.assigned_to.email

        if recipient:
            send_mail(subject, message, 'no-reply@example.com', [recipient])

    @action(detail=False, methods=['GET'])
    def notify_due_tasks(self, request):
        upcoming_tasks = Task.objects.filter(
            due_date__lte=timezone.now() + timedelta(days=2),
            status__in=['pending', 'in_progress'],
            is_deleted=False
        )
        
        for task in upcoming_tasks:
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    f'Task Due Soon: {task.title}',
                    f'The task "{task.title}" is due on {task.due_date}. Please complete it soon.',
                    'no-reply@example.com',
                    [task.assigned_to.email]
                )
        return Response({'message': 'Due date notifications sent.'})

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_deleted = True
        task.save()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_200_OK)