from django.contrib import admin
from django.contrib.auth.models import User
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'created_by')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter the Manager dropdown in the Project table
        if db_field.name == "manager":
            kwargs["queryset"] = User.objects.filter(groups__name="Manager")
            
        # Optional: Filter created_by to only show CTOs/Superusers
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(is_superuser=True)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'main_project', 'status')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter the Assigned To dropdown in the Task table
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(groups__name="Employee")
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)