"""Test the GitHubJob class."""

from unittest import mock

from ... import config
from ...jobs import bases as jobs_bases
from ...jobs import github_job as jobs_module
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


@mock.patch(JOBS_MODULE + ".GithubRepository.download_zip_bundle_files")
class TestGitHubJobJobGetPrecheck(fixtures_git.GitTestHarness):
  """Test the GitHubJob class get_precheck_content method."""

  def setUp(self) -> None:
    super().setUp()
    self.job = jobs_module.GitHubJob(self.repository_http_url, None)

  def test_get_precheck_content_return_value(
      self, m_download: mock.Mock
  ) -> None:
    mock_files = {"a", "b"}
    m_download.return_value = mock_files

    results = self.job.get_precheck_content()
    self.assertEqual(results, mock_files)

  def test_get_precheck_content_call(self, m_download: mock.Mock) -> None:

    self.job.get_precheck_content()

    m_download.assert_called_once_with(
        None,
        {
            'notes': str(config.PRECHECK['notes']),
            'env': str(config.PRECHECK['env']),
        },
    )


@mock.patch(JOBS_MODULE + ".click.echo")
@mock.patch(JOBS_MODULE + ".WorkSpace")
@mock.patch(JOBS_MODULE + ".GithubRepository.download_zip_bundle_profile")
@mock.patch(JOBS_BASES + ".JobSpec.create_job_spec_from_github")
class TestJGitHubJobGetState(fixtures_git.GitTestHarness):
  """Test the GitHubJob class get_state method."""

  def setUp(self) -> None:
    super().setUp()
    self.job = jobs_module.GitHubJob(self.repository_http_url, None)

  def test_get_state_return_value(
      self, m_create: mock.Mock, _: mock.Mock, __: mock.Mock, ___: mock.Mock
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    results = self.job.get_state()

    self.assertEqual(results, mock_spec_content['spec_file_content'])

  def test_get_state_download(
      self, m_create: mock.Mock, m_download: mock.Mock, m_workspace: mock.Mock,
      _: mock.Mock
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.job.get_state()

    m_download.assert_called_once_with(m_workspace.return_value.root, None)

  def test_get_state_echo(
      self, m_create: mock.Mock, _: mock.Mock, __: mock.Mock, m_echo: mock.Mock
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
      self, m_create: mock.Mock, _: mock.Mock, m_workspace: mock.Mock,
      __: mock.Mock
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.job.get_state()

    m_create.assert_called_once_with(m_workspace.return_value)
