"""Logger for the Mac Maker."""

import logging
import sys

from .. import config


class Logger:
  """Mac Maker Logger.

  :parameter debug: a boolean indicating if debug logging should be enabled.
  """

  def __init__(self, debug: bool = False) -> None:
    self.debug = debug
    self.handler = logging.StreamHandler(sys.stdout)
    self.level = self._get_logging_level()
    self.logger = logging.getLogger(config.LOGGER_NAME)

  def _get_logging_level(self) -> int:
    if self.debug:
      return logging.DEBUG
    return logging.WARNING

  def _get_stdout_formatter(self) -> logging.Formatter:
    return logging.Formatter(config.LOGGER_FORMAT)

  def setup(self) -> None:
    """Configure the project's logger."""

    self.logger.setLevel(self.level)
    self.handler.setFormatter(self._get_stdout_formatter())
    self.logger.handlers = []
    self.logger.addHandler(self.handler)
