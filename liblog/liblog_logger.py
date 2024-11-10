#
# This file is part of liblog Python library (https://github.com/io-no/liblog).
# Copyright (c) 2024 Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

import logging

from liblog.internal_liblog import InternalLibLog


class LibLogLogger(logging.Logger):
    """Custom logger class that inherits from the logging.Logger class."""

    internal_liblog: InternalLibLog
    """The internal library logger."""

    def __init__(self: LibLogLogger, name: str) -> None:
        """Initialize the logger.

        Args:
            name (str): The name of the logger.

        Returns:
            None
        """
        self.__internal_liblog = InternalLibLog()
        super().__init__(name)

    def setLevel(self: LibLogLogger, level: int | str) -> None:  # noqa: N802
        """Set the level of the logger.

        Args:
            level (int, str): The level to set.

        Returns:
            None
        """
        # Set the level of the logger
        super().setLevel(level)

        # If the level is lower than the current lowest level, update the lowest level
        # We use self.level instead of level to be sure about the level type
        self.__internal_liblog.lowest_level = min(self.level, self.__internal_liblog.lowest_level)
