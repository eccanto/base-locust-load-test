"""This module defines a spike testing example."""

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


class SpikeTest(StagesShape):
    """Locust shape class defining the spike test stages.

    Attributes:
        stages: List of dictionaries specifying the duration and number of users for each stage.
    """
    stages: ClassVar = [
        {'duration': 10, 'users': 2000},
        {'duration': 90, 'users': 2000},
        {'duration': 3, 'users': 3600},
        {'duration': 3, 'users': 2000},
        {'duration': 120, 'users': 2000},
        {'duration': 3, 'users': 3600},
        {'duration': 3, 'users': 2000},
        {'duration': 90, 'users': 2000},
    ]
