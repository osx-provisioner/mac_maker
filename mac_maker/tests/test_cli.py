"""Test the OSX-Provisioner CLI."""

from typing import Optional
from unittest import mock

from click.testing import CliRunner
from parameterized import parameterized_class
from .. import cli as cli_module
from ..cli import cli
from .fixtures import fixtures_git

CLI_MODULE = cli_module.__name__


class CLITestHarness(fixtures_git.GitTestHarness):
  """Test Harness for CLI Commands."""

  def setUp(self) -> None:
    super().setUp()
    self.runner = CliRunner()


@parameterized_class(
    [
        {
            "branch": None,
            "args": ""
        }, {
            "branch": "develop",
            "args": " --branch=develop"
        }
    ]
)
@mock.patch(CLI_MODULE + ".jobs.GitHubJob")
class TestPrecheckGithub(CLITestHarness):
  """Test the `precheck` CLI command with github repositories."""

  args: str
  branch: Optional[str]

  def test_precheck(self, m_job: mock.Mock) -> None:

    instance = m_job.return_value

    self.runner.invoke(
        cli,
        args=f"precheck github {self.repository_http_url}{self.args}",
    )
    m_job.assert_called_once_with(self.repository_http_url, self.branch)
    instance.precheck.assert_called_once_with()


@mock.patch(CLI_MODULE + ".jobs.FileSystemJob")
class TestPrecheckSpec(CLITestHarness):
  """Test the `precheck` CLI command with spec files."""

  def test_precheck(self, m_job: mock.Mock) -> None:

    instance = m_job.return_value
    mock_spec_file = "/non-existent/path"

    self.runner.invoke(
        cli,
        args=f"precheck spec {mock_spec_file}",
    )
    m_job.assert_called_once_with(mock_spec_file)
    instance.precheck.assert_called_once_with()


@parameterized_class(
    [
        {
            "branch": None,
            "args": ""
        }, {
            "branch": "develop",
            "args": " --branch=develop"
        }
    ]
)
@mock.patch(CLI_MODULE + ".jobs.GitHubJob")
class TestApplyGithub(CLITestHarness):
  """Test the `apply` CLI command with GitHub repositories."""

  args: str
  branch: Optional[str]

  def test_apply(self, m_job: mock.Mock) -> None:
    instance = m_job.return_value

    self.runner.invoke(
        cli,
        args=f"apply github {self.repository_http_url}{self.args}",
    )

    m_job.assert_called_once_with(self.repository_http_url, self.branch)
    instance.precheck.assert_called_once_with()
    instance.provision.assert_called_once_with()


@mock.patch(CLI_MODULE + ".jobs.FileSystemJob")
class TestApplySpec(CLITestHarness):
  """Test the `apply` CLI command with spec files."""

  def test_apply(self, m_job: mock.Mock) -> None:
    instance = m_job.return_value
    mock_spec_file = "/non-existent/path"

    self.runner.invoke(
        cli,
        args=f"apply spec {mock_spec_file}",
    )
    m_job.assert_called_once_with(mock_spec_file)
    instance.precheck.assert_called_once_with()
    instance.provision.assert_called_once_with()


@mock.patch(CLI_MODULE + ".jobs.VersionJob")
class TestVersion(CLITestHarness):
  """Test the `version` CLI command."""

  def test_precheck_call(self, m_command: mock.Mock) -> None:
    instance = m_command.return_value

    self.runner.invoke(
        cli,
        args="version",
    )

    instance.invoke.assert_called_once_with()


@mock.patch(CLI_MODULE + ".Logger")
class TestLoggerIsInitializedWithDebug(CLITestHarness):
  """Test the logger is initialized with debug."""

  def test_precheck_call(self, m_log: mock.Mock) -> None:
    instance = m_log.return_value

    self.runner.invoke(
        cli,
        args="--debug version",
    )

    m_log.assert_called_once_with(debug=True)
    instance.setup.assert_called_once_with()


@mock.patch(CLI_MODULE + ".Logger")
class TestLoggerIsInitializedWithoutDebug(CLITestHarness):
  """Test the logger is initialized without debug."""

  def test_precheck_call(self, m_log: mock.Mock) -> None:
    instance = m_log.return_value

    self.runner.invoke(
        cli,
        args="version",
    )

    m_log.assert_called_once_with(debug=False)
    instance.setup.assert_called_once_with()
