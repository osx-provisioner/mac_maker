"""Test the AnsibleProcess class."""

import shlex
from logging import Logger
from unittest import TestCase, mock

from click_shell.exceptions import ClickShellCleanExit, ClickShellUncleanExit
from ... import config
from ...utilities import filesystem, state
from .. import process

ANSIBLE_PROCESS = process.__name__


class TestAnsibleProcessClass(TestCase):
  """Test instantiating the AnsibleProcess class."""

  def setUp(self):
    self.mock_folder = "/mock/dir1"
    self.mock_module = "ansible.module.mocked"
    self.mock_class = "MockClass"

    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.process = process.AnsibleProcess(
        self.mock_module, self.mock_class,
        self.state.state_generate(self.filesystem)
    )

  def test_init(self):

    self.assertIsInstance(
        self.process.log,
        Logger,
    )
    self.assertEqual(
        self.process.state,
        self.state.state_generate(self.filesystem),
    )
    self.assertEqual(self.process.ansible_module, self.mock_module)
    self.assertEqual(self.process.ansible_class, self.mock_class)


@mock.patch(ANSIBLE_PROCESS + ".os")
@mock.patch(ANSIBLE_PROCESS + ".importlib.import_module")
class TestAnsibleProcessSpawn(TestCase):
  """Test starting the AnsibleRunner class."""

  def setUp(self):
    self.mock_folder = "/mock/dir1"
    self.mock_module = "ansible.module.mocked"
    self.mock_class = "MockClass"
    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.process = process.AnsibleProcess(
        self.mock_module, self.mock_class,
        self.state.state_generate(self.filesystem)
    )

    self.command = "ansible-galaxy install requirements -r requirements.yml"

  def test_spawn_forked_process(self, m_import, m_os):
    split_command = shlex.split(self.command)

    mock_display = mock.Mock()
    mock_cli_module = mock.Mock()
    mock_cli_class = getattr(mock_cli_module, self.mock_class)
    m_import.side_effect = [mock_display, mock_cli_module]

    m_os.fork.return_value = 0

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    m_os.fork.assert_called_once_with()
    mock_cli_class.assert_called_once_with(split_command)
    mock_cli_class.return_value.run.assert_called_once_with()

  def test_spawn_forked_process_dynamic_imports(self, m_import, m_os):

    mock_display = mock.Mock()
    mock_cli_module = mock.Mock()
    m_import.side_effect = [mock_display, mock_cli_module]

    m_os.fork.return_value = 0

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    self.assertEqual(
        m_import.call_args_list, [
            mock.call(config.ANSIBLE_LIBRARY_LOCALE_MODULE),
            mock.call(self.mock_module)
        ]
    )

  @mock.patch(ANSIBLE_PROCESS + ".environment.Environment.setup")
  def test_spawn_forked_process_environment(self, m_env, m_import, m_os):
    m_os.fork.return_value = 0

    mock_display = mock.Mock()
    mock_cli_module = mock.Mock()
    m_import.side_effect = [mock_display, mock_cli_module]

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    m_os.chdir.assert_called_once_with(self.process.state['profile_data_path'])
    mock_display.initialize_locale.assert_called_once_with()
    m_env.assert_called_once_with()

  def test_spawn_forked_process_interrupt(self, _, m_os):
    m_os.fork.return_value = 0
    m_os.chdir.side_effect = KeyboardInterrupt("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

  def test_spawn_forked_process_exception(self, m_import, m_os):
    m_os.fork.return_value = 0

    mock_display = mock.Mock()
    mock_cli_module = mock.Mock()
    mock_cli_class = getattr(mock_cli_module, self.mock_class)
    m_import.side_effect = [mock_display, mock_cli_module]

    mock_cli_class.return_value.run.side_effect = Exception("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

  def test_spawn_main_process(self, _, m_os):
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 0)
    m_os.WEXITSTATUS.return_value = 0

    self.process.spawn(self.command)

    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)

  def test_spawn_main_process_child_error(self, _, m_os):
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 256)
    m_os.WEXITSTATUS.return_value = 1

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)

  def test_spawn_main_process_interrupt(self, _, m_os):
    m_os.fork.return_value = 1
    m_os.waitpid.side_effect = KeyboardInterrupt("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)
