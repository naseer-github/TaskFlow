from django.urls import path
from .views import TaskListCreateAPI, ProjectListCreateAPI, TaskDetailAPI, ProjectDetailAPI, register_user

urlpatterns = [
    # This maps to http://127.0.0.1:8000/tasks/api/
    path('api/', TaskListCreateAPI.as_view(), name='task_list_api'),
    # Project API: http://127.0.0.1:8000/tasks/projects/api/
    path('projects/api/', ProjectListCreateAPI.as_view(), name='project-api'),
    
    # Detail URLs (The <int:pk> captures the ID from the URL)
    path('api/<int:pk>/', TaskDetailAPI.as_view(), name='task-detail'),
    path('projects/api/<int:pk>/', ProjectDetailAPI.as_view(), name='project-detail'),
    
    path('register/', register_user, name='register'),
]
