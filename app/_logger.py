import sys
import loguru


def setup_logger():
    logger = loguru.logger
    logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

    return logger


logger = setup_logger()
