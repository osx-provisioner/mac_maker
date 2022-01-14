"""Test the CLI utilities module."""

import sys
from unittest import TestCase, mock

from .. import cli


class TestCLIUtilities(TestCase):
  """Test the CLI utilities module."""

  @mock.patch.object(sys, 'argv', ["macmaker"])
  def test_was_started_without_shell_false(self) -> None:
    self.assertFalse(cli.was_started_without_shell())

  @mock.patch.object(
      sys, 'argv',
      ["macmaker", "apply", "github", "http://github.com/mock/repository"]
  )
  def test_was_started_without_shell_true(self) -> None:
    self.assertTrue(cli.was_started_without_shell())
