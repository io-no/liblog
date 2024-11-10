#
# This file is part of liblog Python library (https://github.com/io-no/liblog).
# Copyright (c) 2024 Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

import logging

from liblog.utils import get_level_colors


class LogHandler(logging.StreamHandler):
    """Custom log handler to format the log messages."""

    def __init__(self: LogHandler) -> None:
        """Initialize the handler."""
        super().__init__()

    def emit(self: LogHandler, record: logging.LogRecord) -> None:
        """Format the log message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            None
        """
        # Get the colors associated with the logging level
        header_color_set, header_color_reset = get_level_colors(record.levelno)

        # Extract the logger name excluding the root level
        logger_name = ".".join(record.name.split(".")[1:])

        # Format the header
        header = f"[{header_color_set}{logger_name}{header_color_reset}]"

        # Add the header to the message
        record.msg = f"{header} {record.msg}"

        super().emit(record)
