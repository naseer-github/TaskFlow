from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer, EmployeeTaskUpdateSerializer
from drf_spectacular.utils import extend_schema

# ===========================
# 🔐 CUSTOM ROLE PERMISSIONS
# ===========================

class IsCTO(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.groups.filter(name='CTO').exists()


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Employee').exists()


# ===========================
# 📁 PROJECT APIs
# ===========================

@extend_schema(tags=['Projects'])
class ProjectListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='CTO').exists():
            return Project.objects.all().order_by('-created_at')
        if user.groups.filter(name='Manager').exists():
            return Project.objects.filter(manager=user).order_by('-created_at')
        return Project.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.groups.filter(name='CTO').exists()):
            return Response(
                {"error": "Only CTO can create projects"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(tags=['Projects'])
class ProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='CTO').exists():
            return Project.objects.all()
        if user.groups.filter(name='Manager').exists():
            return Project.objects.filter(manager=user)
        return Project.objects.none()


# ===========================
# 📁 TASK APIs
# ===========================

@extend_schema(tags=['Tasks'])
class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='CTO').exists():
            return Task.objects.all().order_by('-created_at')
        if user.groups.filter(name='Manager').exists():
            return Task.objects.filter(main_project__manager=user).order_by('-created_at')
        return Task.objects.filter(assigned_to=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Employee').exists():
            return Response(
                {"error": "Employees cannot create tasks"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['Tasks'])
class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='CTO').exists():
            return Task.objects.all()
        if user.groups.filter(name='Manager').exists():
            return Task.objects.filter(main_project__manager=user)
        return Task.objects.filter(assigned_to=user)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.groups.filter(name='Employee').exists():
            if obj.assigned_to != user:
                raise permissions.PermissionDenied("Not allowed")
        return obj

    def get_serializer_class(self):
        user = self.request.user
        is_cto = user.is_superuser or user.groups.filter(name='CTO').exists()
        is_manager = user.groups.filter(name='Manager').exists()
        if not (is_cto or is_manager):
            return EmployeeTaskUpdateSerializer
        return TaskSerializer


# ===========================
# 👤 USER REGISTRATION
# ===========================

@extend_schema(tags=['Auth'])
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already taken'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': f'User {username} created!'})