"""Test the Jobs class."""

from typing import cast
from unittest import TestCase, mock

from .. import config
from .. import jobs as jobs_module
from ..utilities import precheck, spec, state
from .fixtures import fixtures_git

JOBS_MODULE = jobs_module.__name__


class TestJobs(fixtures_git.GitTestHarness):
  """Test the Jobs class."""

  def test_init(self) -> None:
    self.assertIsInstance(
        self.jobs.jobspec,
        spec.JobSpec,
    )


@mock.patch(JOBS_MODULE + ".GithubRepository.download_zip_bundle_files")
class TestJobsPrecheckFromGithub(fixtures_git.GitTestHarness):
  """Test the Jobs class get_precheck_content_from_github method."""

  def test_get_precheck_return_value(self, m_download: mock.Mock) -> None:
    mock_files = {"a", "b"}
    m_download.return_value = mock_files

    results = self.jobs.get_precheck_content_from_github(
        self.repository_http_url, None
    )

    self.assertEqual(results, mock_files)

  def test_get_precheck_call(self, m_download: mock.Mock) -> None:

    self.jobs.get_precheck_content_from_github(self.repository_http_url, None)

    m_download.assert_called_once_with(
        None,
        {
            'notes': str(config.PRECHECK['notes']),
            'env': str(config.PRECHECK['env']),
        },
    )


@mock.patch(JOBS_MODULE + ".JobSpec.extract_precheck_from_job_spec")
class TestJobsPrecheckFromSpec(fixtures_git.GitTestHarness):
  """Test the Jobs class get_precheck_content_from_spec method."""

  def test_get_precheck_return_value(self, m_extract: mock.Mock) -> None:
    mock_data = {"a", "b"}
    mock_spec_file_location = "/root/spec.json"
    m_extract.return_value = mock_data

    results = self.jobs.get_precheck_content_from_spec(mock_spec_file_location)

    self.assertEqual(results, mock_data)

  def test_get_precheck_call(self, m_extract: mock.Mock) -> None:

    mock_data = {"a", "b"}
    mock_spec_file_location = "/root/spec.json"
    m_extract.return_value = mock_data

    self.jobs.get_precheck_content_from_spec(mock_spec_file_location)

    m_extract.assert_called_once_with(mock_spec_file_location)


@mock.patch(JOBS_MODULE + ".PrecheckConfig")
@mock.patch(JOBS_MODULE + ".click.echo")
class TestJobsPrecheck(fixtures_git.GitTestHarness):
  """Test the Jobs class precheck method."""

  def setUp(self) -> None:
    super().setUp()
    self.mock_precheck_data = precheck.TypePrecheckFileData(
        notes='some notes',
        env='environment test data',
    )

  def test_precheck_echo(self, m_echo: mock.Mock, m_env: mock.Mock) -> None:

    instance = m_env.return_value
    instance.validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    self.jobs.precheck(self.mock_precheck_data)

    m_echo.assert_called_once_with(self.mock_precheck_data['notes'])

  def test_precheck_environment(self, _: mock.Mock, m_env: mock.Mock) -> None:

    instance = m_env.return_value
    instance.validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    self.jobs.precheck(self.mock_precheck_data)

  def test_precheck_environment_invalid(
      self, m_echo: mock.Mock, m_env: mock.Mock
  ) -> None:

    instance = m_env.return_value
    instance.validate_environment.return_value = {
        'is_valid': False,
        'violations': ['violation1', 'violation2'],
    }

    with self.assertRaises(SystemExit):
      self.jobs.precheck(self.mock_precheck_data)

    m_echo.assert_any_call('violation1')
    m_echo.assert_any_call('violation2')
    self.assertEqual(m_echo.call_count, 2)


@mock.patch(JOBS_MODULE + ".click.echo")
@mock.patch(JOBS_MODULE + ".WorkSpace")
@mock.patch(JOBS_MODULE + ".GithubRepository.download_zip_bundle_profile")
@mock.patch(JOBS_MODULE + ".JobSpec.create_job_spec_from_github")
class TestJobsCreateSpecFromGithub(fixtures_git.GitTestHarness):
  """Test the Jobs class get_precheck_content_from_github method."""

  def test_create_spec_return_value(
      self, m_create: mock.Mock, _: mock.Mock, __: mock.Mock, ___: mock.Mock
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    results = self.jobs.create_state_from_github_spec(
        self.repository_http_url, None
    )

    self.assertEqual(results, mock_spec_content['spec_file_content'])

  def test_create_spec_download(
      self, m_create: mock.Mock, m_download: mock.Mock, m_workspace: mock.Mock,
      _: mock.Mock
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.jobs.create_state_from_github_spec(self.repository_http_url, None)

    m_download.assert_called_once_with(m_workspace.return_value.root, None)

  def test_create_spec_echo(
      self, m_create: mock.Mock, _: mock.Mock, __: mock.Mock, m_echo: mock.Mock
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.jobs.create_state_from_github_spec(self.repository_http_url, None)

    m_echo.assert_any_call(config.ANSIBLE_JOB_SPEC_MESSAGE)
    m_echo.assert_any_call(mock_spec_content['spec_file_location'])

  def test_create_spec_call(
      self, m_create: mock.Mock, _: mock.Mock, m_workspace: mock.Mock,
      __: mock.Mock
  ) -> None:
    mock_spec_content = {
        'spec_file_content': {'a', 'b'},
        'spec_file_location': '/root/spec1'
    }
    m_create.return_value = mock_spec_content

    self.jobs.create_state_from_github_spec(self.repository_http_url, None)

    m_create.assert_called_once_with(m_workspace.return_value)


@mock.patch(JOBS_MODULE + ".click.echo")
@mock.patch(JOBS_MODULE + ".JobSpec.create_job_spec_from_filesystem")
class TestJobsCreateSpecFromSpecFile(TestCase):
  """Test the Jobs class create_spec_from_spec_file method."""

  def setUp(self) -> None:
    self.jobs = jobs_module.Jobs()
    self.mock_spec_content = cast(
        spec.TypeSpecFileData, {
            'spec_file_content': {'a', 'b'},
            'spec_file_location': '/root/spec1'
        }
    )

  def test_create_spec_return_value(
      self, m_create: mock.Mock, _: mock.Mock
  ) -> None:
    m_create.return_value = self.mock_spec_content

    results = self.jobs.create_state_from_local_spec_file(
        self.mock_spec_content['spec_file_location'],
    )

    self.assertEqual(results, self.mock_spec_content['spec_file_content'])

  def test_create_spec_echo(
      self, m_create: mock.Mock, m_echo: mock.Mock
  ) -> None:
    m_create.return_value = self.mock_spec_content

    self.jobs.create_state_from_local_spec_file(
        self.mock_spec_content['spec_file_location'],
    )

    m_echo.assert_any_call(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    m_echo.assert_any_call(self.mock_spec_content['spec_file_location'])

  def test_create_spec_call(self, m_create: mock.Mock, __: mock.Mock) -> None:
    m_create.return_value = self.mock_spec_content

    self.jobs.create_state_from_local_spec_file(
        self.mock_spec_content['spec_file_location'],
    )

    m_create.assert_called_once_with(
        self.mock_spec_content['spec_file_location']
    )


@mock.patch(JOBS_MODULE + ".SUDO")
@mock.patch(JOBS_MODULE + ".InventoryFile")
@mock.patch(JOBS_MODULE + ".AnsibleRunner")
class TestJobsProvision(TestCase):
  """Test the Jobs class provision method."""

  def setUp(self) -> None:
    self.jobs = jobs_module.Jobs()
    self.mock_spec_file_content = cast(
        state.TypeState, {'workspace_root_path': '/root/workspace1'}
    )

  def test_provision_inventory(
      self, _: mock.Mock, m_inventory: mock.Mock, __: mock.Mock
  ) -> None:
    instance = m_inventory.return_value

    self.jobs.provision(self.mock_spec_file_content)

    instance.write_inventory_file.assert_called_once_with()

  def test_provision_sudo(
      self, _: mock.Mock, __: mock.Mock, m_sudo: mock.Mock
  ) -> None:
    self.jobs.provision(self.mock_spec_file_content)

    instance = m_sudo.return_value
    instance.prompt_for_sudo.assert_called_once_with()

  def test_provision_ansible(
      self, m_ansible: mock.Mock, __: mock.Mock, m_sudo: mock.Mock
  ) -> None:
    sudo_password = "secret123"
    instance = m_sudo.return_value
    instance.sudo_password = sudo_password

    self.jobs.provision(self.mock_spec_file_content)

    m_ansible.assert_called_once_with(self.mock_spec_file_content,)
