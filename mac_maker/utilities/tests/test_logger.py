"""Test the Logging functions."""

import io
import logging
from unittest import TestCase

from parameterized import parameterized_class
from ... import config
from .. import logger

LOGGING_MODULE = logger.__name__


# pylint: disable=no-member
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
  """Test the Logger class."""

  def setUp(self):
    self.log = logger.Logger(debug=self.debug)

  def test_init_debug(self):
    self.assertEqual(self.debug, self.log.debug)

  def test_init_level(self):
    self.assertEqual(
        self.log.level,
        self.level,
    )

  def test_init_handler(self):
    self.assertIsInstance(self.log.handler, logging.StreamHandler)

  def test_init_logger(self):
    self.assertIsInstance(self.log.logger, logging.Logger)


class TestLoggerMessage(TestCase):
  """Test the writing a message with the logger class."""

  def setUp(self):
    self.stream = io.StringIO()
    self.test_message = "test message"
    self.log = logger.Logger()
    self.log.handler = logging.StreamHandler(self.stream)
    self.log.setup()
    self.log.logger.error(self.test_message)

  def test_log_message(self):

    message = self.stream.getvalue()

    self.assertIn(config.LOGGER_NAME, message)
    self.assertIn(self.test_message, message)
    self.assertIn("ERROR", message)
