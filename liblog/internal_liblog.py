#
# This file is part of liblog Python library (https://github.com/io-no/liblog).
# Copyright (c) 2024 Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

import logging

from liblog.log_handler import LogHandler
from liblog.utils import get_argv


class InternalLibLog:
    """The class to manage the internal operations of the library."""

    argv: list[str]
    """The command line arguments."""

    parent_logger: logging.Logger
    """The parent logger. Any other logger will be a child of this one."""

    registered_loggers: list[logging.Logger]
    """The list of loggers registered in the library."""

    lowest_level: int
    """The lowest level of the loggers."""

    def __new__(cls: InternalLibLog, _: object | None = None) -> InternalLibLog:
        """Create a new instance of the class following the singleton pattern.

        Args:
            _ (object, optional): The custom logger class.

        Returns:
            InternalLibLog: The new instance of the class.
        """
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
            # Set the instance as not initialized
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self: InternalLibLog, logger_class: object | None = None) -> None:
        """Initialize the class.

        Args:
            logger_class (object, optional): The custom logger class.

        Returns:
            None
        """
        if self.__initialized:
            # The class has already been initialized
            return

        # Set the instance as initialized
        self.__initialized = True

        # Cache the command line arguments
        self.argv = get_argv()

        # Set the initial level to DEBUG if debug mode is enabled, otherwise to INFO
        self.lowest_level = logging.DEBUG if self.is_debug_mode_as_argv("liblog") else logging.INFO

        # Set the custom logger class
        if logger_class is not None:
            logging.setLoggerClass(logger_class)

        # Get the parent logger. Any other logger will be a child of this one
        self.parent_logger = logging.getLogger("liblog")

        # Set the level of the parent logger to the initial level
        self.parent_logger.setLevel(self.lowest_level)

        # Add the new level to the logging module
        logging.addLevelName(100, "SILENT")

        # Set the handler of the parent logger
        self.parent_logger.addHandler(LogHandler())

        # Initialize the list of registered loggers
        self.registered_loggers = []

    def is_debug_mode_as_argv(self, logger_name: str) -> bool:
        """Check if the debug mode for the logger has been enabled from the command line.

        Args:
            logger_name (str): The name of the logger to check.

        Returns:
            bool: True if the debug mode is enabled, False otherwise.
        """
        is_debug_mode: bool = False

        if "debug" in self.argv or logger_name in self.argv:
            is_debug_mode = True

        return is_debug_mode

    def register_logger(self: InternalLibLog, name: str) -> logging.Logger:
        """Register a new logger.

        Args:
            name (str): The name of the logger.

        Returns:
            logging.Logger: The new logger.
        """
        # Create a new logger
        child = self.parent_logger.getChild(name)

        # Add the logger to the list of registered loggers
        self.registered_loggers.append(child)

        return child
