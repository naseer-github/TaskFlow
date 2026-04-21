from django.db import models
from django.contrib.auth.models import User


# ===========================
# 📁 PROJECT MODEL
# ===========================

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # CTO creates the project
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cto_projects'
    )
    
    # CTO assigns project to a Manager
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        manager_name = self.manager.username if self.manager else "No Manager"
        return f"Project: {self.name} (Managed by: {manager_name})"


# ===========================
# 📁 TASK MODEL
# ===========================

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=200)

    # Task belongs to a project
    main_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    
    # Manager assigns task to Employee
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='my_tasks'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='TODO'
    )
    
    employee_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        assigned_user = self.assigned_to.username if self.assigned_to else "Unassigned"
        return f"Task: {self.title} -> {assigned_user}"