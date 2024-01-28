"""This module defines a Locust LoadTestShape for performance testing with different duration and user stages."""

from locust import LoadTestShape


class StagesShape(LoadTestShape):
    """Load test shape class that adjusts user count and spawn rate at different stages.

    Attributes:
        stages: A list of dictionaries representing each stage with the keys:
            - duration: Duration of the stage.
            - users: Total user count for the stage.
    """

    stages = []

    def tick(self):
        """Method called on each tick to determine the current stage's user count and spawn rate.

        Returns:
            A tuple containing the current user count and spawn rate (`None` if the test has completed).
        """
        run_time = self.get_run_time()

        duration = 0
        for index, stage in enumerate(self.stages):
            duration += stage['duration']
            if run_time < duration:
                if index == 0:
                    spawn_rate = stage['users'] / stage['duration']
                elif self.stages[index - 1]['users'] == stage['users']:
                    spawn_rate = 0
                else:
                    spawn_rate = abs(self.stages[index - 1]['users'] - stage['users']) / stage['duration']

                return (stage['users'], max(spawn_rate, 10))
            elif stage['duration'] == 0:
                return (stage['users'], stage['users'])

        return None
