from django.contrib import admin
from .models import Task, Info

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'desc', 'status', 'assigned_to', 'deadline', 'estimated_time', 'actual_time', 'complexity']

@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phoneno', 'message']
