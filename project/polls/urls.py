from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from .views import (registeration_view, UserLoginAPIView, TaskUpdateView,
                    Task_create_view, AllTaskListView, TaskDetailView, TaskDeleteView)


app_name = 'polls'
urlpatterns = [
    path('register', registeration_view, name="register"),
    path('login', UserLoginAPIView.as_view(), name="login"),
    path('task', Task_create_view, name='task-list-create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/all/', AllTaskListView.as_view(), name='all-task-list'),
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),

]
