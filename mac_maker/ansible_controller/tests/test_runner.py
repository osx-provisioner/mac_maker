"""Test the AnsibleRunner class."""

from logging import Logger
from unittest import TestCase, mock

from ... import config
from ...utilities import filesystem, state
from .. import runner

RUNNER_MODULE = runner.__name__


class TestAnsibleRunnerClass(TestCase):
  """Test instantiating the AnsibleRunner class."""

  def setUp(self) -> None:
    self.mock_folder = "/mock/dir1"
    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.ansible = runner.AnsibleRunner(
        self.state.state_generate(self.filesystem)
    )

  def test_init(self) -> None:

    self.assertIsInstance(
        self.ansible.log,
        Logger,
    )
    self.assertEqual(
        self.ansible.state,
        self.state.state_generate(self.filesystem),
    )
    self.assertFalse(self.ansible.debug)


@mock.patch(RUNNER_MODULE + ".click.echo")
@mock.patch(RUNNER_MODULE + ".process.AnsibleProcess")
class TestAnsibleRunnerSequence(TestCase):
  """Test starting the AnsibleRunner class."""

  def setUp(self) -> None:
    self.mock_folder = "/mock/dir1"
    self.mock_state = {
        "one": "two"
    }
    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.ansible = runner.AnsibleRunner(
        self.state.state_generate(self.filesystem)
    )

  def test_spawn(self, m_process: mock.Mock, _: mock.Mock) -> None:
    galaxy_mock_roles = mock.Mock()
    galaxy_mock_collections = mock.Mock()
    playbook_mock = mock.Mock()
    m_process.side_effect = [
        galaxy_mock_roles,
        galaxy_mock_collections,
        playbook_mock,
    ]

    self.ansible.start()

    self.assertEqual(
        m_process.call_args_list, [
            mock.call(
                config.ANSIBLE_LIBRARY_GALAXY_MODULE,
                config.ANSIBLE_LIBRARY_GALAXY_CLASS,
                self.ansible.state,
            ),
            mock.call(
                config.ANSIBLE_LIBRARY_GALAXY_MODULE,
                config.ANSIBLE_LIBRARY_GALAXY_CLASS,
                self.ansible.state,
            ),
            mock.call(
                config.ANSIBLE_LIBRARY_PLAYBOOK_MODULE,
                config.ANSIBLE_LIBRARY_PLAYBOOK_CLASS,
                self.ansible.state,
            ),
        ]
    )

    requirements_file_path = self.filesystem.get_galaxy_requirements_file(
    ).resolve()
    roles_file_path = self.filesystem.get_roles_path().resolve()
    collections_file_path = self.filesystem.get_collections_path().resolve()

    galaxy_mock_roles.spawn.assert_called_once_with(
        "ansible-galaxy role install -r"
        f" {requirements_file_path}"
        f" -p {roles_file_path}"
    )

    galaxy_mock_collections.spawn.assert_called_once_with(
        "ansible-galaxy collection install -r"
        f" {requirements_file_path}"
        f" -p {collections_file_path}"
    )

    playbook_mock.spawn.assert_called_once_with(
        "ansible-playbook"
        f" {self.filesystem.get_playbook_file().resolve()}"
        f" -i {self.filesystem.get_inventory_file()}"
        " -e "
        "\"ansible_become_password="
        "'{{ lookup('env', 'ANSIBLE_BECOME_PASSWORD') }}'\""
    )

  def test_ansible_command_debug(
      self, m_process: mock.Mock, _: mock.Mock
  ) -> None:
    galaxy_mock_roles = mock.Mock()
    galaxy_mock_collections = mock.Mock()
    playbook_mock = mock.Mock()
    m_process.side_effect = [
        galaxy_mock_roles,
        galaxy_mock_collections,
        playbook_mock,
    ]

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
