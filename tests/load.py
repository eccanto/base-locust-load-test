"""This module defines a load testing example."""

from typing import ClassVar

from locust import HttpUser, between

from base import StagesShape, UserTasks


class WebsiteUser(HttpUser):
    """Locust user class for simulating website users.

    Attributes:
        wait_time: Tuple specifying the wait time between tasks.
        tasks: List of TaskSets to be executed by the user.
    """
    wait_time = between(0, 1)
    tasks: ClassVar = [UserTasks]


class LoadTest(StagesShape):
    """Locust shape class defining the load test stages.

    Attributes:
        stages: List of dictionaries specifying the duration and number of users for each stage.
    """
    stages: ClassVar = [
        {'duration': 90, 'users': 2400},
        {'duration': 120, 'users': 2400},
        {'duration': 90, 'users': 0},
    ]
