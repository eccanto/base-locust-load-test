"""Example Locustfile."""

import os

from locust import HttpUser, between, events, task
from locust.runners import MasterRunner


@events.init.add_listener
def on_locust_init(environment, **_):
    """Registers callbacks to locust.

    :param environment: Locust environment.
    """
    if isinstance(environment.runner, MasterRunner):
        environment.runner.register_message('user_finished', MasterEvents.on_user_finished)


@events.init_command_line_parser.add_listener
def _(parser):
    """Adds arguments to the Locust command line.

    :param parser: Locust arguments parser.
    """
    parser.add_argument(
        '-i',
        '--iterations',
        type=int,
        env_var='USER_ITERATIONS',
        help='Number of iterations by user',
    )


class MasterEvents:  # pylint: disable=too-few-public-methods
    """Class that contains the locust master callbacks."""

    _FINISHED_USERS = 0

    @classmethod
    def on_user_finished(cls, msg, environment):  # pylint: disable=unused-argument
        """Callback used to notify that a user has finished.

        :param msg: Notify message.
        :param environment: Locust environment.
        """
        cls._FINISHED_USERS += 1

        if cls._FINISHED_USERS == environment.runner.target_user_count:
            environment.runner.stop()


class TestUsers(HttpUser):
    """Class to test the endpoint /api/users."""

    _API_USERNAME = os.environ['API_USERNAME']
    _API_PASSWORD = os.environ['API_PASSWORD']

    wait_time = between(0, 1)

    def __init__(self, *args, **kwargs):
        """Constructor method."""
        super().__init__(*args, **kwargs)

        self.jwt_token = None

        self.iteration = 0
        self.max_iterations = self.environment.parsed_options.iterations

    def on_start(self):
        """Called when a simulated user starts executing that TaskSet."""
        response = self.client.get('/api/token', auth=(self._API_USERNAME, self._API_PASSWORD))
        self.jwt_token = response.json()['access']

    @task
    def get_users(self):
        """Task to test the endpoint /api/users."""
        if self.iteration < self.max_iterations:
            self.iteration += 1

            self.client.get('/api/users', headers={'Authorization': f'JWT {self.jwt_token}'})
        else:
            self.environment.runner.send_message('user_finished', 'done!')
            self.environment.runner.greenlet.join()
