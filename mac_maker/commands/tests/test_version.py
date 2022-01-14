"""Test the VersionCommand class."""

from unittest import TestCase, mock

import pkg_resources
from .. import version
from ..version import VersionCommand

VERSION_MODULE = version.__name__


@mock.patch(VERSION_MODULE + ".click.echo")
class TestVersionCommand(TestCase):
  """Test the VersionCommand class."""

  def setUp(self) -> None:
    self.command = VersionCommand()

  def test_get_version(self, m_echo: mock.Mock) -> None:
    self.command.get_version()

    m_echo.assert_called_once_with(
        "Mac Maker Version: "
        f"{pkg_resources.get_distribution('mac_maker').version}",
    )
