from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.Api.views import TaskInfoViewSet

router = DefaultRouter()
router.register('taskInfo', TaskInfoViewSet, basename='taskInfo')

urlpatterns = [
    path('api/', include(router.urls)),
]
