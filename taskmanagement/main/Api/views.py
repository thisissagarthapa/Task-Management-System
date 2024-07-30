from main.models import Task
from .serializers import TaskSerializers
from rest_framework import viewsets

class TaskInfoViewSet(viewsets.ModelViewSet):
    queryset=Task.objects.all()
    serializer_class=TaskSerializers