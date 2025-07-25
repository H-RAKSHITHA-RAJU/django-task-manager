# task_manager/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # For login/logout
    path('', include('tasks.urls')), # Include your app's URLs
]