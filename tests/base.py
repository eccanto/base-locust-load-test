"""This module defines a Locust LoadTestShape for performance testing with different duration and user stages."""

import os
from typing import ClassVar

from locust import LoadTestShape, TaskSet, task


class ObtainJWTError(Exception):
    """Raised when failed to obtain JWT token."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__('Failed to obtain JWT token')


class UserTasks(TaskSet):
    """TaskSet for simulating user interactions with API endpoints.

    Attributes:
        _API_USERNAME (str): The API username obtained from the environment variable 'API_USERNAME'.
        _API_PASSWORD (str): The API password obtained from the environment variable 'API_PASSWORD'.
    """

    _API_USERNAME = os.environ['API_USERNAME']
    _API_PASSWORD = os.environ['API_PASSWORD']

    @task
    def get_users(self) -> None:
        """Sends a GET request to the endpoint "/api/users".

        Raises:
            ValueError: If failed to obtain the JWT token.
        """
        response = self.client.get('/api/token', auth=(self._API_USERNAME, self._API_PASSWORD))
        if response.ok:
            jwt_token = response.json()['access']
            self.client.get('/api/users', headers={'Authorization': f'JWT {jwt_token}'})
        else:
            raise ObtainJWTError


class StagesShape(LoadTestShape):
    """Load test shape class that adjusts user count and spawn rate at different stages.

    Attributes:
        stages: A list of dictionaries representing each stage with the keys:
            - duration: Duration of the stage.
            - users: Total user count for the stage.
    """

    stages: ClassVar = []

    def tick(self) -> tuple[int, float] | None:
        """Method called on each tick to determine the current stage's user count and spawn rate.

        Returns:
            A tuple containing the current user count and spawn rate (`None` if the test has completed).
        """
        run_time = self.get_run_time()

        duration = 0
        tick_data = None
        for index, stage in enumerate(self.stages):
            duration += stage['duration']

            if run_time < duration:
                if index == 0:
                    spawn_rate = stage['users'] / stage['duration']
                elif self.stages[index - 1]['users'] == stage['users']:
                    spawn_rate = 0
                else:
                    spawn_rate = abs(self.stages[index - 1]['users'] - stage['users']) / stage['duration']

                tick_data = (stage['users'], max(spawn_rate, 10))
                break

            if stage['duration'] == 0:
                tick_data = (stage['users'], stage['users'])
                break

        return tick_data
