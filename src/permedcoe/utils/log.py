import logging

LOG_LEVEL_DEBUG = "debug"
LOG_LEVEL_INFO = "info"
LOG_LEVEL_WARNING = "warning"
LOG_LEVEL_ERROR = "error"
LOG_LEVEL_CRITICAL = "critical"

LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def init_logging(debug=False, level=LOG_LEVEL_ERROR):
    """Initialize logging.
    Supported levels: ["debug" | "info" | "warning" | "error" | "critical"]

    Args:
        debug (bool, optional): Force debug mode.
        level (str, optional): Log level. Defaults to LOG_LEVEL_ERROR.
    """
    if debug:
        log_level = logging.DEBUG
    else:
        # Select the logging level
        if level == LOG_LEVEL_CRITICAL:
            log_level = logging.CRITICAL
        elif level == LOG_LEVEL_ERROR:
            log_level = logging.ERROR
        elif level == LOG_LEVEL_WARNING:
            log_level = logging.WARNING
        elif level == LOG_LEVEL_INFO:
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
    # Initialize logging
    logging.basicConfig(level=log_level, format=LOGGING_FORMAT)
