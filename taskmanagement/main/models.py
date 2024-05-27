from django.db import models

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title=models.CharField(max_length=50)
    desc=models.TextField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES)
    assigned_to = models.CharField(max_length=50)
    deadline = models.DateField()
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
    
