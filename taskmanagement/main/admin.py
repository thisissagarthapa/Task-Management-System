from django.contrib import admin
from .models import Task
from .models import Info
# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display =['id','desc','status','assigned_to','deadline']
    
@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display=['id','name','email','phoneno','message']
    
