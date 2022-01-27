"""Test the GitHubJob class."""

from unittest import mock

from ... import config
from ...jobs import bases as jobs_bases
from ...jobs import github as jobs_module
from ...tests.fixtures import fixtures_git

JOBS_MODULE = jobs_module.__name__
JOBS_BASES = jobs_bases.__name__


class TestGitHubJob(fixtures_git.GitTestHarness):
  """Test the GitHubJob class."""

  def setUp(self) -> None:
    super().setUp()
    self.mock_branch = "mock_branch"
    self.job = jobs_module.GitHubJob(self.repository_http_url, self.mock_branch)

  def test_init(self) -> None:
    self.assertEqual(self.job.branch_name, self.mock_branch)
    self.assertIsNone(self.job.workspace)
    self.assertEqual(self.job.repository_url, self.repository_http_url)


@mock.patch(JOBS_MODULE + ".WorkSpace")
@mock.patch(JOBS_MODULE + ".GithubRepository.download_zip_bundle_profile")
@mock.patch(JOBS_BASES + ".JobSpecExtractor.get_job_spec_data")
@mock.patch(JOBS_BASES + ".PrecheckExtractor.get_precheck_data")
class TestGitHubJobGetPrecheck(fixtures_git.GitTestHarness):
  """Test the GitHubJob class get_precheck_content method."""

  def setUp(self) -> None:
    super().setUp()
    self.job = jobs_module.GitHubJob(self.repository_http_url, None)
    self.mock_spec_contents = "mock spec contents"
    self.mock_spec_file_location = "/mock/path"
    self.mock_spec_data = dict(
        spec_file_content=self.mock_spec_contents,
        spec_file_location=self.mock_spec_file_location,
    )
    self.mock_precheck_data = dict(
        notes="None.",
        env=[],
    )

  def test_get_precheck_content_return_value(
      self,
      m_precheck: mock.Mock,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
  ) -> None:
    m_precheck.return_value = self.mock_precheck_data

    results = self.job.get_precheck_content()
    self.assertEqual(results, self.mock_precheck_data)

  def test_get_precheck_content_calls(
      self,
      m_precheck: mock.Mock,
      m_spec: mock.Mock,
      m_download: mock.Mock,
      m_workspace: mock.Mock,
  ) -> None:
    m_precheck.return_value = self.mock_precheck_data
    m_spec.return_value = self.mock_spec_data
    m_workspace.return_value.spec_file = self.mock_spec_file_location

    self.job.get_precheck_content()

    m_workspace.return_value.add_spec_file.assert_called_once_with()
    m_spec.assert_called_once_with(m_workspace.return_value.spec_file)
    m_download.assert_called_once_with(m_workspace.return_value.root, None)
    m_precheck.assert_called_once_with(self.mock_spec_data)

  def download_not_called_twice(
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
@mock.patch(JOBS_BASES + ".JobSpecExtractor.get_job_spec_data")
class TestGitHubJobGetState(fixtures_git.GitTestHarness):
  """Test the GitHubJob class get_state method."""

  def setUp(self) -> None:
    super().setUp()
    self.job = jobs_module.GitHubJob(self.repository_http_url, None)
    self.mock_spec_file_location = '/root/spec1'
    self.mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': self.mock_spec_file_location
    }

  def test_get_state_return_value(
      self,
      m_job: mock.Mock,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
  ) -> None:
    m_job.return_value = self.mock_spec_content

    results = self.job.get_state()

    self.assertEqual(results, self.mock_spec_content['spec_file_content'])

  def test_get_state_download(
      self,
      m_job: mock.Mock,
      m_download: mock.Mock,
      m_workspace: mock.Mock,
      _: mock.Mock,
  ) -> None:
    m_job.return_value = self.mock_spec_content

    self.job.get_state()

    m_download.assert_called_once_with(m_workspace.return_value.root, None)

  def test_get_state_echo(
      self,
      m_job: mock.Mock,
      _: mock.Mock,
      __: mock.Mock,
      m_echo: mock.Mock,
  ) -> None:
    m_job.return_value = self.mock_spec_content

    self.job.get_state()

    m_echo.assert_any_call(config.ANSIBLE_JOB_SPEC_MESSAGE)
    m_echo.assert_any_call(self.mock_spec_content['spec_file_location'])

  def test_get_job_spec_call(
      self,
      m_job: mock.Mock,
      _: mock.Mock,
      m_workspace: mock.Mock,
      __: mock.Mock,
  ) -> None:
    m_job.return_value = self.mock_spec_content
    m_workspace.return_value.spec_file = self.mock_spec_file_location

    self.job.get_state()

    m_workspace.return_value.add_spec_file.assert_called_once_with()
    m_job.assert_called_once_with(self.mock_spec_file_location)

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
