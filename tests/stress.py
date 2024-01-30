"""This module defines a stress testing example."""

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


class StressTest(StagesShape):
    """Locust shape class defining the stress test stages.

    Attributes:
        stages: List of dictionaries specifying the duration and number of users for each stage.
    """
    stages: ClassVar = [
        {'duration': 300, 'users': 3600},
    ]
