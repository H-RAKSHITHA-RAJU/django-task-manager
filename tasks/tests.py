# tasks/tests.py
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class TaskAPITests(APITestCase):
    # This method runs before every single test
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        # Log the user in. self.client is a virtual web browser provided by APITestCase
        self.client.login(username='testuser', password='testpassword123')
        # The URL for our API list/create endpoint
        self.list_create_url = reverse('api-task-list')

    def test_unauthenticated_user_cannot_access_api(self):
        """
        Ensure unauthenticated users are denied access (get a 403 Forbidden).
        """
        # First, log out the user we logged in during setUp
        self.client.logout()
        # Make a request to the API
        response = self.client.get(self.list_create_url)
        # Check that the status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_list_tasks(self):
        """
        Ensure an authenticated user can retrieve a list of their tasks.
        """
        response = self.client.get(self.list_create_url)
        # Check that the request was successful (200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_task(self):
        """
        Ensure an authenticated user can create a new task via the API.
        """
        # The data for the new task we want to create
        task_data = {
            'title': 'Test API Task',
            'description': 'This is a test description.',
        }
        # Make a POST request to the API to create the task
        response = self.client.post(self.list_create_url, task_data, format='json')
        # Check that the task was created successfully (201 CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the task's title in the response matches what we sent
        self.assertEqual(response.data['title'], 'Test API Task')
        # Check that the task was correctly assigned to our user
        self.assertEqual(response.data['user'], self.user.id)