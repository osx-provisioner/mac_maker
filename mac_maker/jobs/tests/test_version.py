"""Test the VersionJob class."""

from importlib.metadata import version as metadata_version
from unittest import mock

from mac_maker.jobs import version


class TestVersionJob:
  """Test the VersionJob class."""

  def test_invoke__calls_echo(
      self, mocked_click_echo: mock.Mock,
      version_job_instance: version.VersionJob
  ) -> None:
    version_job_instance.invoke()

    mocked_click_echo.assert_called_once_with(
        f"Mac Maker Version: {metadata_version('mac_maker')}",
    )
