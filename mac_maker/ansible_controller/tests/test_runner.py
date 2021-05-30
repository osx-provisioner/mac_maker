"""Test the AnsibleRunner class."""

from logging import Logger
from unittest import TestCase, mock

from ...utilities import filesystem, state
from .. import runner

RUNNER_MODULE = runner.__name__


class TestAnsibleRunnerClass(TestCase):
  """Test instantiating the AnsibleRunner class."""

  def setUp(self):
    self.mock_folder = "/mock/dir1"
    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.ansible = runner.AnsibleRunner(
        self.state.state_generate(self.filesystem)
    )

  def test_init(self):

    self.assertIsInstance(
        self.ansible.log,
        Logger,
    )
    self.assertEqual(
        self.ansible.state,
        self.state.state_generate(self.filesystem),
    )
    self.assertFalse(self.ansible.debug)


@mock.patch(RUNNER_MODULE + ".GalaxyCLI")
@mock.patch(RUNNER_MODULE + ".PlaybookCLI")
@mock.patch(RUNNER_MODULE + ".click.echo")
@mock.patch(RUNNER_MODULE + ".AnsibleProcess")
class TestAnsibleRunnerSequence(TestCase):
  """Test starting the AnsibleRunner class."""

  def setUp(self):
    self.mock_folder = "/mock/dir1"
    self.mock_state = {
        "one": "two"
    }
    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.ansible = runner.AnsibleRunner(
        self.state.state_generate(self.filesystem)
    )

  def test_spawn(self, m_process, _, m_play, m_galaxy):
    galaxy_mock = mock.Mock()
    playbook_mock = mock.Mock()
    m_process.side_effect = [galaxy_mock, playbook_mock]

    self.ansible.start()

    m_process.assert_any_call(m_galaxy, self.ansible.state)
    m_process.assert_any_call(m_play, self.ansible.state)

    self.assertEqual(m_process.call_count, 2)

    galaxy_mock.spawn.assert_called_once_with(
        "ansible-galaxy install -r"
        f" {self.filesystem.get_galaxy_requirements_file().resolve()}"
        f" --roles-path={self.filesystem.get_roles_path().resolve()}"
    )

    playbook_mock.spawn.assert_called_once_with(
        "ansible-playbook"
        f" {self.filesystem.get_playbook_file().resolve()}"
        f" -i {self.filesystem.get_inventory_file()}"
        " -e "
        "\"ansible_become_password="
        "'{{ lookup('env', 'ANSIBLE_BECOME_PASSWORD') }}'\""
    )

  def test_ansible_command_debug(self, m_process, _, __, ___):
    playbook_mock = mock.Mock()
    m_process.side_effect = [mock.Mock(), playbook_mock]

    self.ansible.debug = True
    self.ansible.start()

    playbook_mock.spawn.assert_called_once_with(
        "ansible-playbook"
        f" {self.filesystem.get_playbook_file().resolve()}"
        f" -i {self.filesystem.get_inventory_file()}"
        " -e "
        "\"ansible_become_password="
        "'{{ lookup('env', 'ANSIBLE_BECOME_PASSWORD') }}'\""
        " -vvvv"
    )
