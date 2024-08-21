from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    desc = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField()
    estimated_time = models.FloatField()  # Estimated time to complete the task
    actual_time = models.FloatField(null=True, blank=True)  # Actual time taken to complete the task
    complexity = models.IntegerField()  # Task complexity (e.g., scale 1-10)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class Info(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneno = models.CharField(max_length=30)
    message = models.TextField()

    def __str__(self):
        return self.name
    
