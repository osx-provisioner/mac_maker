"""Test the Logger class."""

import io
import logging
from typing import cast
from unittest import TestCase

from parameterized import parameterized_class
from ... import config
from .. import logger

LOGGING_MODULE = logger.__name__


@parameterized_class(
    [
        {
            "debug": True,
            "level": logging.DEBUG
        }, {
            "debug": False,
            "level": logging.WARNING
        }
    ]
)
class TestLoggerDebug(TestCase):
  """Test initializing Logging class."""

  log: logger.Logger
  level: bool

  def setUp(self) -> None:
    self.log = logger.Logger(debug=cast(bool, self.debug))

  def test_init_debug(self) -> None:
    self.assertEqual(self.debug, self.log.debug)

  def test_init_level(self) -> None:
    self.assertEqual(
        self.log.level,
        self.level,
    )

  def test_init_handler(self) -> None:
    self.assertIsInstance(self.log.handler, logging.StreamHandler)

  def test_init_logger(self) -> None:
    self.assertIsInstance(self.log.logger, logging.Logger)


class TestLoggerMessage(TestCase):
  """Test writing a message with the Logger class."""

  def setUp(self) -> None:
    self.stream = io.StringIO()
    self.test_message = "test message"
    self.log = logger.Logger()
    self.log.handler = logging.StreamHandler(self.stream)
    self.log.setup()
    self.log.logger.error(self.test_message)

  def test_log_message(self) -> None:

    message = self.stream.getvalue()

    self.assertIn(config.LOGGER_NAME, message)
    self.assertIn(self.test_message, message)
    self.assertIn("ERROR", message)
