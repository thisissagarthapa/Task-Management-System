from main.models import Task
from rest_framework import serializers

class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'