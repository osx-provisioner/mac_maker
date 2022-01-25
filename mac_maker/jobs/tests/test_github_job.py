"""Test the GitHubJob class."""

from unittest import mock

from ... import config
from ...jobs import bases as jobs_bases
from ...jobs import github as jobs_module
from ...tests.fixtures import fixtures_git
from ...utilities import spec

JOBS_MODULE = jobs_module.__name__
JOBS_BASES = jobs_bases.__name__


class TestGitHubJob(fixtures_git.GitTestHarness):
  """Test the GitHubJob class."""

  def setUp(self) -> None:
    super().setUp()
    self.job = jobs_module.GitHubJob(self.repository_http_url, None)

  def test_init(self) -> None:
    self.assertIsInstance(
        self.job.jobspec,
        spec.JobSpec,
    )
    self.assertIsNone(self.job.branch_name)
    self.assertEqual(self.repository_http_url, self.job.repository_url)


@mock.patch(JOBS_MODULE + ".WorkSpace")
@mock.patch(JOBS_MODULE + ".GithubRepository.download_zip_bundle_profile")
@mock.patch(JOBS_BASES + ".JobSpec.read_job_spec_from_workspace")
@mock.patch(JOBS_BASES + ".JobSpec.extract_precheck_from_job_spec")
class TestGitHubJobJobGetPrecheck(fixtures_git.GitTestHarness):
  """Test the GitHubJob class get_precheck_content method."""

  def setUp(self) -> None:
    super().setUp()
    self.job = jobs_module.GitHubJob(self.repository_http_url, None)

  def test_get_precheck_content_return_value(
      self,
      m_job: mock.Mock,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
  ) -> None:
    m_job.return_value = "mock spec contents"

    results = self.job.get_precheck_content()
    self.assertEqual(results, m_job.return_value)

  def test_get_precheck_content_calls(
      self,
      m_job: mock.Mock,
      m_spec: mock.Mock,
      m_download: mock.Mock,
      m_workspace: mock.Mock,
  ) -> None:
    mock_spec_data = dict(
        spec_file_content="mock spec contents",
        spec_file_location="/mock/path",
    )
    m_spec.return_value = mock_spec_data

    self.job.get_precheck_content()

    m_spec.assert_called_once_with(m_workspace.return_value)
    m_job.assert_called_once_with(mock_spec_data['spec_file_location'])
    m_download.assert_called_once_with(m_workspace.return_value.root, None)

  def test_download_not_called_twice(
      self,
      _: mock.Mock,
      __: mock.Mock,
      m_download: mock.Mock,
      m_workspace: mock.Mock,
  ) -> None:
    self.job.get_precheck_content()
    self.job.get_precheck_content()
    m_download.assert_called_once_with(m_workspace.return_value.root, None)


@mock.patch(JOBS_MODULE + ".click.echo")
@mock.patch(JOBS_MODULE + ".WorkSpace")
@mock.patch(JOBS_MODULE + ".GithubRepository.download_zip_bundle_profile")
@mock.patch(JOBS_BASES + ".JobSpec.read_job_spec_from_workspace")
class TestJGitHubJobGetState(fixtures_git.GitTestHarness):
  """Test the GitHubJob class get_state method."""

  def setUp(self) -> None:
    super().setUp()
    self.job = jobs_module.GitHubJob(self.repository_http_url, None)

  def test_get_state_return_value(
      self,
      m_create: mock.Mock,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    results = self.job.get_state()

    self.assertEqual(results, mock_spec_content['spec_file_content'])

  def test_get_state_download(
      self,
      m_create: mock.Mock,
      m_download: mock.Mock,
      m_workspace: mock.Mock,
      _: mock.Mock,
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.job.get_state()

    m_download.assert_called_once_with(m_workspace.return_value.root, None)

  def test_get_state_echo(
      self,
      m_create: mock.Mock,
      _: mock.Mock,
      __: mock.Mock,
      m_echo: mock.Mock,
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.job.get_state()

    m_echo.assert_any_call(config.ANSIBLE_JOB_SPEC_MESSAGE)
    m_echo.assert_any_call(mock_spec_content['spec_file_location'])

  def test_get_state_call(
      self,
      m_create: mock.Mock,
      _: mock.Mock,
      m_workspace: mock.Mock,
      __: mock.Mock,
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.job.get_state()

    m_create.assert_called_once_with(m_workspace.return_value)

  def test_download_not_called_twice(
      self,
      _: mock.Mock,
      m_download: mock.Mock,
      m_workspace: mock.Mock,
      __: mock.Mock,
  ) -> None:
    self.job.get_state()
    self.job.get_state()
    m_download.assert_called_once_with(m_workspace.return_value.root, None)
