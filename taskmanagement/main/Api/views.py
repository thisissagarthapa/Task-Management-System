from main.models import Task
from .serializers import TaskSerializers
from rest_framework import viewsets, status
from rest_framework.response import Response

class TaskInfoViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

    def create(self, request, *args, **kwargs):
        # Expecting a list of task objects
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
