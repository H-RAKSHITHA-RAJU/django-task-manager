# tasks/views.py

# Django and Python imports
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic

# Django REST Framework imports
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Local application imports
from .models import Task
from .serializers import TaskSerializer

# --- User Authentication Views ---

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# --- Web-based CRUD Views (for HTML templates) ---

# tasks/views.py

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Start with all tasks for the logged-in user
        user_tasks = Task.objects.filter(user=self.request.user)

        # Get the filter parameter from the URL (e.g., /?filter=incomplete)
        filter_by = self.request.GET.get('filter', None)

        if filter_by == 'incomplete':
            # If the filter is 'incomplete', only get tasks where completed is False
            return user_tasks.filter(completed=False).order_by('-created_at')
        elif filter_by == 'complete':
            # If the filter is 'complete', only get tasks where completed is True
            return user_tasks.filter(completed=True).order_by('-created_at')

        # If no filter is specified, return all tasks
        return user_tasks.order_by('-created_at')
class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        # Check if the user trying to access the task is the owner
        task = self.get_object()
        return self.request.user == task.user

class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'completed']
    success_url = reverse_lazy('task-list') # This redirects to the URL named 'task-list'

    def form_valid(self, form):
        # Set the current logged-in user as the owner of the task
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'completed']
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

# --- API Views (for JSON data) ---

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit their tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)