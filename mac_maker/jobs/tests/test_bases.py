"""Test the Jobs base class."""

from typing import cast
from unittest import TestCase, mock

from ...utilities import precheck, spec, state
from .. import bases as bases_module

BASES_MODULE = bases_module.__name__


class MockConcreteJob(bases_module.JobBase):
  """Concrete test implementation of the JobBase class."""

  def __init__(self) -> None:
    super().__init__()
    self.mock_precheck_content = cast(spec.TypePrecheckFileData, {})
    self.mock_state = cast(state.TypeState, {})

  def get_precheck_content(self) -> spec.TypePrecheckFileData:
    return self.mock_precheck_content

  def get_state(self) -> state.TypeState:
    return self.mock_state


class TestJobsBase(TestCase):
  """Test the JobBase class."""

  def setUp(self) -> None:
    self.concrete_job = MockConcreteJob()

  def test_init(self) -> None:
    self.assertIsInstance(
        self.concrete_job.jobspec,
        spec.JobSpec,
    )


@mock.patch(BASES_MODULE + ".PrecheckConfig")
@mock.patch(BASES_MODULE + ".click.echo")
class TestJobsPrecheck(TestCase):
  """Test the JobBase class precheck method."""

  def setUp(self) -> None:
    super().setUp()
    self.concrete_job = MockConcreteJob()
    self.concrete_job.mock_precheck_content = precheck.TypePrecheckFileData(
        notes='some notes',
        env='environment test data',
    )

  def test_precheck_echo(self, m_echo: mock.Mock, m_env: mock.Mock) -> None:

    instance = m_env.return_value
    instance.validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    self.concrete_job.precheck()

    m_echo.assert_called_once_with(
        self.concrete_job.mock_precheck_content['notes']
    )

  def test_precheck_environment(self, _: mock.Mock, m_env: mock.Mock) -> None:

    instance = m_env.return_value
    instance.validate_environment.return_value = {
        'is_valid': True,
        'violations': [],
    }

    self.concrete_job.precheck()

  def test_precheck_environment_invalid(
      self, m_echo: mock.Mock, m_env: mock.Mock
  ) -> None:

    instance = m_env.return_value
    instance.validate_environment.return_value = {
        'is_valid': False,
        'violations': ['violation1', 'violation2'],
    }

    with self.assertRaises(SystemExit):
      self.concrete_job.precheck()

    m_echo.assert_any_call('violation1')
    m_echo.assert_any_call('violation2')
    self.assertEqual(m_echo.call_count, 2)


@mock.patch(BASES_MODULE + ".SUDO")
@mock.patch(BASES_MODULE + ".InventoryFile")
@mock.patch(BASES_MODULE + ".AnsibleRunner")
class TestJobsProvision(TestCase):
  """Test the JobBase class provision method."""

  def setUp(self) -> None:
    self.concrete_job = MockConcreteJob()
    self.mock_state = cast(
        state.TypeState, {'workspace_root_path': '/root/workspace1'}
    )
    self.concrete_job.mock_state = self.mock_state

  def test_provision_inventory(
      self, _: mock.Mock, m_inventory: mock.Mock, __: mock.Mock
  ) -> None:
    instance = m_inventory.return_value

    self.concrete_job.provision()

    instance.write_inventory_file.assert_called_once_with()

  def test_provision_sudo(
      self, _: mock.Mock, __: mock.Mock, m_sudo: mock.Mock
  ) -> None:
    self.concrete_job.provision()

    instance = m_sudo.return_value
    instance.prompt_for_sudo.assert_called_once_with()

  def test_provision_ansible(
      self, m_ansible: mock.Mock, __: mock.Mock, m_sudo: mock.Mock
  ) -> None:
    sudo_password = "secret123"
    instance = m_sudo.return_value
    instance.sudo_password = sudo_password

    self.concrete_job.provision()

    m_ansible.assert_called_once_with(self.mock_state,)