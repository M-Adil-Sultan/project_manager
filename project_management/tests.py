from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Project, Task
from datetime import date, timedelta

class ProjectManagementTests(TestCase):

    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

        # Authenticate the client
        self.client.login(username='testuser', password='testpassword')

        # Create a sample project
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project.'
        )

    def authenticate_client(self):
        # Obtain JWT tokens
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.token = response.data['access']
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        print(response.data)

    def test_create_project(self):
        self.authenticate_client()
        response = self.client.post(reverse('project-list'), {
            'name': 'New Project',
            'description': 'A newly created project.'
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.count(), 2)
        print(response.data)


    def test_update_project(self):
        self.authenticate_client()
        update_url = reverse('project-detail', args=[self.project.id])
        response = self.client.put(update_url, {
            'name': 'Updated Project',
            'description': 'Updated description.'
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project')
        print(response.data)


    


    def test_create_task(self):
        self.authenticate_client()
        task_data = {
            'project': self.project.id,
            'title': 'New Task',
            'description': 'Task description',
            'status': 'pending',
            'priority': 'high',
            'due_date': date.today() + timedelta(days=5)
        }
        response = self.client.post(reverse('task-list'), task_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        print(response.data)


    def test_update_task(self):
        self.authenticate_client()
        # Create a task first
        task = Task.objects.create(
            project=self.project,
            title='Initial Task',
            description='Initial description',
            due_date=date.today() + timedelta(days=5)
        )
        update_url = reverse('task-detail', args=[task.id])
        response = self.client.put(update_url, {
            'project': self.project.id,
            'title': 'Updated Task Title',
            'description': 'Updated description.',
            'status': 'in_progress',
            'priority': 'medium',
            'due_date': date.today() + timedelta(days=7)
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task Title')
        self.assertEqual(task.status, 'in_progress')
        print(response.data)


    def test_assign_task_to_user(self):
        self.authenticate_client()
        # Create a task
        task = Task.objects.create(
            project=self.project,
            title='Task for Assignment',
            description='Description of the task',
            due_date=date.today() + timedelta(days=5)
        )
        assign_url = reverse('task-detail', args=[task.id])
        response = self.client.put(assign_url, {
            'project': self.project.id,
            'assigned_to': self.user.id,
            'status': task.status,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date,
            'priority': task.priority
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.assigned_to, self.user)
        print(response.data)


    def test_user_authentication(self):
        # Obtain JWT tokens
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        print(response.data)

    def test_delete_project(self):
        self.authenticate_client()
        delete_url = reverse('project-detail', args=[self.project.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertTrue(self.project.is_deleted)
        print(response.data)

