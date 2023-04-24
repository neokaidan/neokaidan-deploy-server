import logging
import logging.config
import logging.handlers

import config as cfg

LOG_SCOPE = "gacd_server"
LOG_LEVEL = "INFO"
LOG_FILE = "gacd_server.log"


def get_logger(configuration: cfg.Configuration):
    log = logging.getLogger(__name__)

    log_format = f"[%(asctime)s] [ {LOG_SCOPE} ] [%(levelname)s]:%(name)s:%(message)s"

    logging.basicConfig(
        filename=configuration.logs_path + LOG_FILE,
        filemode="a",
        level=LOG_LEVEL,
        format=log_format
    )

    return log
