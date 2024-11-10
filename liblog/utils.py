#
# This file is part of liblog Python library (https://github.com/io-no/liblog).
# Copyright (c) 2024 Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import inspect
import logging
import sys


def get_caller_package_name() -> str:
    """Get the package name of the calling module.

    Returns:
        str: The package name of the calling module.
    """
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


def get_argv() -> list[str]:
    """Get the command line arguments.

    Returns:
        list[str]: The command line arguments.
    """
    return [arg.lower() for arg in sys.argv]


def get_level_colors(levelno: int) -> str:
    """Get the colors associated with the logging level.

    Args:
        levelno (int): The logging level number.

    Returns:
        tuple(str, str): The color to set and the color to reset.
    """
    header_color_set = ""
    if levelno >= logging.CRITICAL:
        # Blinking red
        header_color_set = "\033[91m"
    elif levelno >= logging.ERROR:
        # Red
        header_color_set = "\033[91m"
    elif levelno >= logging.WARNING:
        # Yellow
        header_color_set = "\033[93m"
    elif levelno >= logging.INFO:
        # Green
        header_color_set = "\033[92m"
    elif levelno >= logging.DEBUG:
        # Blue
        header_color_set = "\033[94m"

    header_color_reset = "\033[0m"

    return header_color_set, header_color_reset
