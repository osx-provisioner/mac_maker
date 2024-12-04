"""Test the VersionCommand class."""

from importlib.metadata import version
from unittest import TestCase, mock

from .. import version as jobs_module

JOBS_MODULE = jobs_module.__name__


@mock.patch(JOBS_MODULE + ".click.echo")
class TestVersionCommand(TestCase):
  """Test the VersionCommand class."""

  def setUp(self) -> None:
    self.command = jobs_module.VersionJob()

  def test_invoke(self, m_echo: mock.Mock) -> None:
    self.command.invoke()

    m_echo.assert_called_once_with(
        f"Mac Maker Version: {version('mac_maker')}",
    )
