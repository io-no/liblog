#
# Copyright (c) 2024 Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import inspect
import logging


def get_caller_package_name() -> str:
    """Get the package name of the calling module."""
    # Get the current frame, then go back in the stack to find the caller
    frame = inspect.currentframe()

    # Go back two frames to reach the caller's frame
    caller_frame = frame.f_back.f_back

    # Get the module name from the caller's frame
    caller_module = inspect.getmodule(caller_frame)

    found_name = "Unknown"

    # Retrieve the package name from the module
    if caller_module and caller_module.__package__:
        found_name = caller_module.__package__
    elif caller_module:
        # If no package, return the module's name
        found_name = caller_module.__name__
    return found_name


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
