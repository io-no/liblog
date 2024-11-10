#
# Copyright (c) 2024 Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

import logging

from liblog.internal_liblog import InternalLibLog
from liblog.liblog_logger import LibLogLogger
from liblog.utils import get_caller_package_name


class LibLog:
    """A class to manage logging in packages in an easy way."""

    def __init__(self: LibLog) -> None:
        """Initialize the LibLog class."""
        # Initialize the internal library logger
        self.__internal_liblog = InternalLibLog(LibLogLogger)

    def debug(self: LibLog, msg: str, *args: any, **kwargs: any) -> None:
        """Log a message with severity 'DEBUG' on the logger.

        Args:
            msg (str): The message to log.
            *args (any): The arguments to pass to the logger.
            **kwargs (any): The keyword arguments to pass to the logger.

        Returns:
            None
        """
        if self.__internal_liblog.lowest_level <= logging.DEBUG:
            # There is at least one logger with a level of DEBUG or lower.
            # We try to log the message with the logger of the caller package.
            logger = self.getLogger()
            return logger.debug(msg, *args, **kwargs)
        return None

    def info(self: LibLog, msg: str, *args: any, **kwargs: any) -> None:
        """Log a message with severity 'INFO' on the logger.

        Args:
            msg (str): The message to log.
            *args (any): The arguments to pass to the logger.
            **kwargs (any): The keyword arguments to pass to the logger.

        Returns:
            None
        """
        if self.__internal_liblog.lowest_level <= logging.INFO:
            # There is at least one logger with a level of INFO or lower.
            # We try to log the message with the logger of the caller package.
            logger = self.getLogger()
            return logger.info(msg, *args, **kwargs)
        return None

    def warning(self: LibLog, msg: str, *args: any, **kwargs: any) -> None:
        """Log a message with severity 'WARNING' on the logger.

        Args:
            msg (str): The message to log.
            *args (any): The arguments to pass to the logger.
            **kwargs (any): The keyword arguments to pass to the logger.

        Returns:
            None
        """
        if self.__internal_liblog.lowest_level <= logging.WARNING:
            # There is at least one logger with a level of WARNING or lower.
            # We try to log the message with the logger of the caller package.
            logger = self.getLogger()
            return logger.warning(msg, *args, **kwargs)
        return None

    def error(self: LibLog, msg: str, *args: any, **kwargs: any) -> None:
        """Log a message with severity 'ERROR' on the logger.

        Args:
            msg (str): The message to log.
            *args (any): The arguments to pass to the logger.
            **kwargs (any): The keyword arguments to pass to the logger.

        Returns:
            None
        """
        if self.__internal_liblog.lowest_level <= logging.ERROR:
            # There is at least one logger with a level of ERROR or lower.
            # We try to log the message with the logger of the caller package.
            logger = self.getLogger()
            return logger.error(msg, *args, **kwargs)
        return None

    def critical(self: LibLog, msg: str, *args: any, **kwargs: any) -> None:
        """Log a message with severity 'CRITICAL' on the logger.

        Args:
            msg (str): The message to log.
            *args (any): The arguments to pass to the logger.
            **kwargs (any): The keyword arguments to pass to the logger.

        Returns:
            None
        """
        if self.__internal_liblog.lowest_level <= logging.CRITICAL:
            # There is at least one logger with a level of CRITICAL or lower.
            # We try to log the message with the logger of the caller package.
            logger = self.getLogger()
            return logger.critical(msg, *args, **kwargs)
        return None

    def exception(self: LibLog, msg: str, *args: any, exc_info: bool = True, **kwargs: any) -> None:
        """Log a message with severity 'ERROR' on the logger with exception information.

        Args:
            msg (str): The message to log.
            *args (any): The arguments to pass to the logger.
            exc_info (bool): If True, exception information will be added to the logging message.
            **kwargs (any): The keyword arguments to pass to the logger.

        Returns:
            None
        """
        if self.__internal_liblog.lowest_level <= logging.ERROR:
            # There is at least one logger with a level of ERROR or lower.
            # We try to log the message with the logger of the caller package.
            logger = self.getLogger()
            return logger.exception(msg, *args, exc_info=exc_info, **kwargs)
        return None

    def getLogger(self: LibLog, name: str | None = None) -> logging.Logger:  # noqa: N802
        """Get the logger for the caller package. If the logger does not exist, it will be created.

        Args:
            name (str, optional): The name of the logger. If None, the package name of the calling module will be used.

        Returns:
            logging.Logger: The logger.
        """
        if name is None:
            # Get the package name of the calling module
            name = get_caller_package_name()

        if getattr(self, name, None) is None:
            # The logger does not exist. We create it.
            logger = self.__internal_liblog.register_logger(name)
            setattr(self, name, logger)
        else:
            # The logger already exists. We get it.
            logger = getattr(self, name)
        return logger

    def registerPackage(self: LibLog) -> logging.Logger:  # noqa: N802
        """Force the registration of a new logger for the caller package.

        Returns:
            logging.Logger: The logger of the package.
        """
        return self.getLogger()

    def registerChild(self: LibLog, suffix: str) -> logging.Logger:  # noqa: N802
        """Register a child logger with the given name.

        The parent logger will be the logger of the caller package.

        Args:
            suffix (str): The suffix to add to the parent logger name. It will be the name of the child logger.

        Returns:
            logging.Logger: The child logger.
        """
        # Get the logger corresponding to the caller package
        parent_logger = self.getLogger()

        # Get the child logger
        child_logger = parent_logger.getChild(suffix)

        # Set the child logger as an attribute of LibLog
        setattr(self, suffix, child_logger)

        # Register the child logger in the internal library logger
        self.__internal_liblog.registered_loggers.append(child_logger)

        return child_logger

    def getChild(self: LibLog, name: str) -> logging.Logger:  # noqa: N802
        """Get the child logger with the given name.

        Args:
            name (str): The name of the child logger.

        Returns:
            logging.Logger: The child logger.
        """
        return getattr(self, name)

    def setLevel(self: LibLog, level: int | str) -> None:  # noqa: N802
        """Set the level of the logger of the caller package.

        Note: Any package logger child will inherit this level if its level is not explicitly set.

        Args:
            level (int, str): The level to set. It can be an integer or a string.

        Returns:
            None
        """
        logger = self.getLogger()
        logger.setLevel(level)

    def setGlobalLevel(self: LibLog, level: int | str) -> None:  # noqa: N802
        """Set the global level of the library.

        Note: All liblog loggers will be forced to this level, regardless of the level set in the logger.

        Args:
            level (int, str): The level to set. It can be an integer or a string.
        """
        self.__internal_liblog.parent_logger.setLevel(level)

        for logger in self.__internal_liblog.registered_loggers:
            logger.setLevel(level)
