import os
from dotenv import load_dotenv


class Configuration:
    SHARED_FILE = ".env.shared"
    SECRET_FILE = ".env.secret"

    PORT_ENV = "PORT"
    LOGS_PATH_ENV = "LOGS_PATH"
    AUTH_SECRET_ENV = "AUTH_SECRET"
    DOCKER_SOCKET_ENV = "DOCKER_SOCKET"

    def __init__(self):
        if not load_dotenv(Configuration.SHARED_FILE):
            raise EnvironmentError("Missed or empty '%s' file" % Configuration.SHARED_FILE)
        if not load_dotenv(Configuration.SECRET_FILE):
            raise EnvironmentError("Missed or empty '%s' file" % Configuration.SECRET_FILE)

        self.server_port: str = os.getenv(Configuration.PORT_ENV, None)
        self.logs_path: str = os.getenv(Configuration.LOGS_PATH_ENV, None)
        self.auth_secret: str = os.getenv(Configuration.AUTH_SECRET_ENV, None)
        self.docker_socket: str = os.getenv(Configuration.DOCKER_SOCKET_ENV, None)

        if self.server_port is None:
            raise EnvironmentError("Missed '%s' environment variable" % Configuration.PORT_ENV)

        if self.logs_path is None:
            raise EnvironmentError("Missed '%s' environment variable" % Configuration.LOGS_PATH_ENV)
        else:
            # add trailing slash if it's not already set
            self.logs_path = os.path.join(self.logs_path, "")

        if self.auth_secret is None:
            raise EnvironmentError("Missed '%s' environment variable" % Configuration.AUTH_SECRET_ENV)

        if self.docker_socket is None:
            raise EnvironmentError("Missed '%s' environment variable" % Configuration.DOCKER_SOCKET_ENV)
