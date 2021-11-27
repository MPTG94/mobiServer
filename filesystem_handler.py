import logging
import os
import tempfile

logger = logging.getLogger('gcp_logger')


def create_temp_dir():
    temp_dir = tempfile.TemporaryDirectory()
    logger.warning(f"This tmp dir was created: {temp_dir.name}")
    return temp_dir.name


def create_sub_folders_in_path(directory):
    try:
        if not os.path.exists(directory):
            logger.warning(f"creating directory path: {directory}")
            os.makedirs(directory)
    except OSError:
        logger.warning(f"ERROR: failed to create directory path: {directory}")
