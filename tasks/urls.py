# tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SignUpView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskViewSet,
)

# Create a router and register our viewset with it.
router = DefaultRouter()

# --- THE FIX IS HERE ---
# We change basename='task' to basename='api-task' to prevent name conflicts.
router.register(r'tasks', TaskViewSet, basename='api-task')

urlpatterns = [
    # Signup URL
    path('signup/', SignUpView.as_view(), name='signup'),

    # Web View (Template-based) URLs
    path('', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

    # API URLs (These will now have names like 'api-task-list')
    path('api/', include(router.urls)),
]