#
# Copyright (c) 2024 Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import inspect
import logging


def get_caller_package_name() -> str:
    """Get the package name of the calling module."""
    # Get the current frame
    frame = inspect.currentframe()

    # Get the outer frames
    frames = inspect.getouterframes(frame)

    for f in frames:
        # We find the first frame that is not from the liblog package and return its package name
        if (
            f is not None
            and (module := inspect.getmodule(f[0])) is not None
            and (package := module.__package__) != "liblog"
        ):
            return package
    return "Unknown"


class LibLog:
    """A class to manage logging in a library."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(LibLog, cls).__new__(cls)
            logging.addLevelName(100, "SILENT")
        return cls.instance

    def __init__(self):
        package_name = get_caller_package_name()
        self.set_logger(package_name)

    def set_logger(self, name, level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(logging.StreamHandler())

    def get_logger(self):
        package_name = get_caller_package_name()
        return logging.getLogger(package_name)

    def set_child(self, name):
        package_name = get_caller_package_name()
        parent_logger = logging.getLogger(package_name)
        child_logger = parent_logger.getChild(name)
        # add attribute to parent logger
        setattr(parent_logger, name, child_logger)
