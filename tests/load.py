"""This module defines a load testing example."""

import os

from locust import HttpUser, TaskSet, between, task

from base import StagesShape


class UserTasks(TaskSet):
    """TaskSet for simulating user interactions with API endpoints.

    Attributes:
        _API_USERNAME (str): The API username obtained from the environment variable 'API_USERNAME'.
        _API_PASSWORD (str): The API password obtained from the environment variable 'API_PASSWORD'.
    """

    _API_USERNAME = os.environ['API_USERNAME']
    _API_PASSWORD = os.environ['API_PASSWORD']

    @task
    def get_users(self):
        """Sends a GET request to the endpoint "/api/users".

        Raises:
            ValueError: If failed to obtain the JWT token.
        """
        response = self.client.get('/api/token', auth=(self._API_USERNAME, self._API_PASSWORD))
        if response.ok:
            jwt_token = response.json()['access']
            self.client.get('/api/users', headers={'Authorization': f'JWT {jwt_token}'})
        else:
            raise ValueError('Failed to obtain JWT token.')


class WebsiteUser(HttpUser):
    """Locust user class for simulating website users.

    Attributes:
        wait_time: Tuple specifying the wait time between tasks.
        tasks: List of TaskSets to be executed by the user.
    """
    wait_time = between(0, 1)
    tasks = [UserTasks]


class LoadTest(StagesShape):
    """Locust shape class defining the load test stages.

    Attributes:
        stages: List of dictionaries specifying the duration and number of users for each stage.
    """
    stages = [
        {'duration': 90, 'users': 2400},
        {'duration': 120, 'users': 2400},
        {'duration': 90, 'users': 0},
    ]
