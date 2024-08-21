from django.urls import path
from .views import predict_completion_time
urlpatterns = [
    path('predict/',predict_completion_time,name='predict')
]
