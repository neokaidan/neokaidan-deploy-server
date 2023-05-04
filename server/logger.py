import os
import logging
import logging.config
import logging.handlers
import pathlib

from .config import Configuration

LOG_SCOPE = "gacd_server"
LOG_LEVEL = "INFO"
LOG_FILE = "gacd_server.log"


def get_logger(configuration: Configuration):
    log = logging.getLogger(__name__)

    log_format = f"[%(asctime)s] [ {LOG_SCOPE} ] [%(levelname)s]:%(name)s:%(message)s"

    logs_abs_path = configuration.logs_path
    if not os.path.isabs(configuration.logs_path):
        logs_abs_path = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), configuration.logs_path)

    os.makedirs(os.path.dirname(logs_abs_path), exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(logs_abs_path, LOG_FILE),
        filemode="a",
        level=LOG_LEVEL,
        format=log_format
    )

    return log
