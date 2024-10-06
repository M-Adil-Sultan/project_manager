from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
]
