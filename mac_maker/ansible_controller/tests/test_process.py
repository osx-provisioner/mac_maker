"""Test the AnsibleProcess class."""

import shlex
from logging import Logger
from typing import Type, cast
from unittest import TestCase, mock

from ansible.cli import CLI
from click_shell.exceptions import ClickShellCleanExit, ClickShellUncleanExit
from ... import config
from ...utilities import filesystem, state
from .. import process

ANSIBLE_PROCESS = process.__name__


class TestAnsibleProcessClass(TestCase):
  """Test instantiating the AnsibleProcess class."""

  def setUp(self):
    self.mock_folder = "/mock/dir1"
    self.mock_cli = mock.Mock()
    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.process = process.AnsibleProcess(
        cast(Type[CLI], self.mock_cli),
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
    self.assertIsNone(self.process.pid)
    self.assertEqual(self.process.ansible_cli_class, self.mock_cli)


@mock.patch(ANSIBLE_PROCESS + ".os")
@mock.patch(ANSIBLE_PROCESS + ".initialize_locale")
class TestAnsibleProcessSpawn(TestCase):
  """Test starting the AnsibleRunner class."""

  def setUp(self):
    self.mock_folder = "/mock/dir1"
    self.mock_cli = mock.Mock()
    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.process = process.AnsibleProcess(
        cast(Type[CLI], self.mock_cli),
        self.state.state_generate(self.filesystem)
    )

    self.command = "ansible-galaxy install requirements -r requirements.yml"

  def test_spawn_forked_process(self, _, m_os):
    split_command = shlex.split(self.command)

    m_os.fork.return_value = 0

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    m_os.fork.assert_called_once_with()
    self.mock_cli.assert_called_once_with(split_command)
    self.mock_cli.return_value.run.assert_called_once_with()

  def test_spawn_forked_process_environment(self, m_locale, m_os):
    m_os.fork.return_value = 0

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    m_os.chdir.assert_called_once_with(self.process.state['profile_data_path'])
    m_locale.assert_called_once_with()
    m_os.environ.__setitem__.assert_called_once_with(
        config.ENV_ANSIBLE_ROLES_PATH,
        ":".join(self.process.state['roles_path']),
    )

  def test_spawn_forked_process_interrupt(self, _, m_os):
    m_os.fork.return_value = 0
    m_os.chdir.side_effect = KeyboardInterrupt("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

  def test_spawn_forked_process_exception(self, _, m_os):
    m_os.fork.return_value = 0
    self.mock_cli.return_value.run.side_effect = Exception("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

  def test_spawn_main_process(self, _, m_os):
    m_os.fork.return_value = 1

    self.process.spawn(self.command)

    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)

  def test_spawn_main_process_interrupt(self, _, m_os):
    m_os.fork.return_value = 1
    m_os.waitpid.side_effect = KeyboardInterrupt("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)
