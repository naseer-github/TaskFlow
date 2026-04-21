from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Task


# ===========================
# 📁 TASK SERIALIZER
# ===========================

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name="Employee"),
        help_text="Only users in the Employee group are shown here."
    )

    main_project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.none()
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'main_project', 'assigned_to', 'employee_notes', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if not request:
            return

        user = request.user

        # CTO → all projects
        if user.is_superuser or user.groups.filter(name='CTO').exists():
            self.fields['main_project'].queryset = Project.objects.all()

        # Manager → only their projects
        elif user.groups.filter(name='Manager').exists():
            self.fields['main_project'].queryset = Project.objects.filter(manager=user)

        # Employee → no projects (they shouldn’t create tasks anyway)
        else:
            self.fields['main_project'].queryset = Project.objects.none()


# ===========================
# 📁 PROJECT SERIALIZER
# ===========================

class ProjectSerializer(serializers.ModelSerializer):
    # Show username in GET
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    # 🔒 Prevent manual setting of creator
    created_by = serializers.ReadOnlyField(source='created_by.id')

    # Only Managers selectable
    manager = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name="Manager"),
        allow_null=True,
        required=False,
        help_text="Only users in the Manager group are shown here."
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'manager', 'created_by', 'created_by_username', 'created_at']


# ===========================
# 👨‍💻 EMPLOYEE RESTRICTED SERIALIZER
# ===========================

class EmployeeTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # Employee can only update these
        fields = ['status', 'employee_notes']