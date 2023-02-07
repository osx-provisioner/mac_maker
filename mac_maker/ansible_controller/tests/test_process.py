"""Test the AnsibleProcess class."""

import logging
import shlex
from logging import Logger
from typing import List
from unittest import TestCase, mock

from ... import config
from ...utilities import filesystem, state
from .. import process

PROCESS_MODULE = process.__name__


class TestAnsibleProcessClass(TestCase):
  """Test instantiating the AnsibleProcess class."""

  def setUp(self) -> None:
    self.mock_folder = "/mock/dir1"
    self.mock_module = "ansible.module.mocked"
    self.mock_class = "MockClass"

    self.filesystem = filesystem.FileSystem(self.mock_folder)
    self.state = state.State()
    self.process = process.AnsibleProcess(
        self.mock_module, self.mock_class,
        self.state.state_generate(self.filesystem)
    )

  def test_init(self) -> None:

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


@mock.patch(PROCESS_MODULE + ".os")
@mock.patch(PROCESS_MODULE + ".importlib.import_module")
@mock.patch(PROCESS_MODULE + ".cmd_loop")
@mock.patch(PROCESS_MODULE + ".environment.Environment.setup")
class TestAnsibleProcessSpawn(TestCase):
  """Test the spawn method of an AnsibleProcess instance."""

  def setUp(self) -> None:
    mock_folder = "/mock/dir1"
    mock_class = "MockClass"

    self.mock_module = "ansible.module.mocked"
    self.mock_logger = mock.Mock()
    self.state = state.State()
    self.process = process.AnsibleProcess(
        self.mock_module, mock_class,
        self.state.state_generate(filesystem.FileSystem(mock_folder))
    )

    self.mock_cli_module = mock.Mock()
    self.mock_cli_class = getattr(self.mock_cli_module, mock_class)

    self.command = "ansible-galaxy install requirements -r requirements.yml"

  def logs_for_forked_process(self) -> List[str]:
    return [
        (
            "DEBUG:mac_maker:AnsibleProcess: "
            "Preparing to Fork for Ansible Process."
        ),
        (
            "DEBUG:mac_maker:AnsibleProcess - PID: 0: "
            f"Forked process is now executing: {self.command}."
        ),
        (
            "DEBUG:mac_maker:AnsibleProcess - PID: 0: "
            "Forked process Ansible CLI Class instance has been "
            f"created: {self.mock_cli_class.return_value}."
        ),
        (
            "DEBUG:mac_maker:AnsibleProcess - PID: 0: "
            "Forked process Ansible CLI Class instance is calling run."
        ),
        (
            "DEBUG:mac_maker:AnsibleProcess - PID: 0: "
            "Forked process has finished."
        )
    ]

  def logs_for_main_process_without_error(self) -> List[str]:
    return [
        (
            "DEBUG:mac_maker:AnsibleProcess: "
            "Preparing to Fork for Ansible Process."
        ),
        (
            "DEBUG:mac_maker:AnsibleProcess - PID: 1: "
            "Waited, and received exit code: 0."
        ),
        (
            "DEBUG:mac_maker:AnsibleProcess - PID: 1: "
            "Forked process has reported no error state."
        ),
    ]

  def logs_for_main_process_with_error(self) -> List[str]:
    return self.logs_for_main_process_without_error()[0:1] + [
        (
            "DEBUG:mac_maker:AnsibleProcess - PID: 1: "
            "Waited, and received exit code: 1."
        ),
        (
            "ERROR:mac_maker:AnsibleProcess - PID: 1: "
            "Forked process has reported an error state."
        ),
    ]

  def logs_for_main_process_with_interrupt(self) -> List[str]:
    return self.logs_for_main_process_without_error()[0:1] + [
        (
            "ERROR:mac_maker:AnsibleProcess - PID: 1: "
            "Keyboard Interrupt Intercepted."
        )
    ]

  def test__spawn__forked_process(
      self,
      _: mock.Mock,
      m_cmdloop: mock.Mock,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    split_command = shlex.split(self.command)
    m_import.side_effect = [self.mock_cli_module]
    m_os.fork.return_value = 0

    self.process.spawn(self.command)

    m_os.fork.assert_called_once_with()
    m_cmdloop.exit_shell.assert_called_once_with(0, 0)
    self.mock_cli_class.assert_called_once_with(split_command)
    self.mock_cli_class.return_value.run.assert_called_once_with()

  def test__spawn__forked_process__logs(
      self,
      _: mock.Mock,
      __: mock.Mock,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_import.side_effect = [self.mock_cli_module]
    m_os.fork.return_value = 0

    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.process.spawn(self.command)

    self.assertEqual(
        logs.output,
        self.logs_for_forked_process(),
    )

  def test__spawn__forked_process__dynamic_imports(
      self,
      _: mock.Mock,
      m_cmdloop: mock.Mock,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_import.side_effect = [self.mock_cli_module]
    m_os.fork.return_value = 0

    self.process.spawn(self.command)

    m_cmdloop.exit_shell.assert_called_once_with(0, 0)
    self.assertEqual(m_import.call_args_list, [mock.call(self.mock_module)])

  def test__spawn__forked_process__environment(
      self,
      m_env: mock.Mock,
      m_cmdloop: mock.Mock,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_import.side_effect = [self.mock_cli_module]

    self.process.spawn(self.command)

    m_env.assert_called_once_with()
    m_cmdloop.exit_shell.assert_called_once_with(0, 0)
    m_os.chdir.assert_called_once_with(self.process.state['profile_data_path'])

  def test__spawn__forked_process__interrupt(
      self,
      _: mock.Mock,
      m_cmdloop: mock.Mock,
      __: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_os.chdir.side_effect = KeyboardInterrupt("Boom!")

    self.process.spawn(self.command)

    m_cmdloop.exit_shell.assert_called_once_with(
        self.process.error_exit_code, 0
    )

  def test__spawn__forked_process__interrupt__logs(
      self,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_os.chdir.side_effect = KeyboardInterrupt("Boom!")

    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.process.spawn(self.command)

    self.assertEqual(
        logs.output,
        self.logs_for_forked_process()[0:2],
    )

  def test__spawn__forked_process__exception(
      self,
      _: mock.Mock,
      m_cmdloop: mock.Mock,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_import.side_effect = [self.mock_cli_module]
    self.mock_cli_class.return_value.run.side_effect = Exception("Boom!")

    self.process.spawn(self.command)

    m_cmdloop.exit_shell.assert_called_once_with(
        self.process.error_exit_code, 0
    )

  def test__spawn__forked_process__exception__logs(
      self,
      _: mock.Mock,
      __: mock.Mock,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_import.side_effect = [self.mock_cli_module]
    self.mock_cli_class.return_value.run.side_effect = Exception("Boom!")

    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.process.spawn(self.command)

    self.assertEqual(
        logs.output,
        self.logs_for_forked_process()[0:4],
    )

  def test__spawn__main_process(
      self,
      _: mock.Mock,
      m_cmdloop: mock.Mock,
      __: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 0)
    m_os.WEXITSTATUS.return_value = 0

    self.process.spawn(self.command)

    m_cmdloop.exit_shell.assert_not_called()
    m_cmdloop.exit.assert_not_called()
    m_cmdloop.interrupt.assert_not_called()
    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)

  def test__spawn__main_process__logs(
      self,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 0)
    m_os.WEXITSTATUS.return_value = 0

    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.process.spawn(self.command)

    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)
    self.assertEqual(
        logs.output,
        self.logs_for_main_process_without_error(),
    )

  def test__spawn__main_process__child_error(
      self,
      _: mock.Mock,
      m_cmdloop: mock.Mock,
      __: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 256)
    m_os.WEXITSTATUS.return_value = 1

    self.process.spawn(self.command)

    m_cmdloop.exit_shell.assert_not_called()
    m_cmdloop.exit.assert_called_with(1, 1)
    m_cmdloop.interrupt.assert_not_called()
    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)

  def test__spawn__main_process__child_error__logs(
      self,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 256)
    m_os.WEXITSTATUS.return_value = 1

    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.process.spawn(self.command)

    self.assertEqual(
        logs.output,
        self.logs_for_main_process_with_error(),
    )

  def test__spawn__main_process__interrupt(
      self,
      _: mock.Mock,
      m_cmdloop: mock.Mock,
      __: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.side_effect = KeyboardInterrupt("Boom!")

    self.process.spawn(self.command)

    m_cmdloop.exit_shell.assert_not_called()
    m_cmdloop.exit.assert_called_with(self.process.error_exit_code, 1)
    m_cmdloop.interrupt.assert_not_called()

  def test__spawn__main_process_interrupt__logs(
      self,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.side_effect = KeyboardInterrupt("Boom!")

    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.process.spawn(self.command)

    self.assertEqual(
        logs.output,
        self.logs_for_main_process_with_interrupt(),
    )
