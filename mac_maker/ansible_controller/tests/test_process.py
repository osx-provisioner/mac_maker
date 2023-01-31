"""Test the AnsibleProcess class."""

import shlex
from logging import Logger
from typing import List, Tuple
from unittest import TestCase, mock

from click_shell.exceptions import ClickShellCleanExit, ClickShellUncleanExit
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

    self.process.log = mock.Mock()
    self.mock_cli_module = mock.Mock()
    self.mock_cli_class = getattr(self.mock_cli_module, mock_class)

    self.command = "ansible-galaxy install requirements -r requirements.yml"

  def subtest_log_content(
      self,
      expected_content: List[Tuple[str, str]],
  ) -> None:
    received_content: List[Tuple[str, str]] = []

    for level in ["debug", "info", "warning", "error", "critical"]:
      mock_logger: mock.Mock = getattr(self.process.log, level)
      for call in mock_logger.call_args_list:  # pylint: disable=no-member
        received_content.append((
            level,
            call.args[0] % call.args[1:],
        ))

    self.assertListEqual(received_content, expected_content)

  def logs_for_forked_process(self) -> List[Tuple[str, str]]:
    return [
        (
            "debug",
            "AnsibleProcess: Preparing to Fork for Ansible Process.",
        ),
        (
            "debug",
            (
                "AnsibleProcess - PID: 0: Forked process is now "
                f"executing: {self.command}."
            ),
        ),
        (
            "debug",
            (
                "AnsibleProcess - PID: 0: Forked process Ansible CLI Class "
                "instance has been "
                f"created: {self.mock_cli_class.return_value}."
            ),
        ),
        (
            "debug",
            (
                "AnsibleProcess - PID: 0: Forked process Ansible CLI Class "
                "instance is calling run."
            ),
        ),
        (
            "debug",
            ("AnsibleProcess - PID: 0: Forked process has finished."),
        ),
    ]

  def logs_for_forked_process_without_shell(self) -> List[Tuple[str, str]]:
    log_content = self.logs_for_forked_process()
    log_content.append(
        (
            "warning",
            ("AnsibleProcess - PID: 0: Terminating process."),
        )
    )
    return log_content

  def logs_for_main_process_without_error(self) -> List[Tuple[str, str]]:
    return [
        (
            "debug",
            ("AnsibleProcess: Preparing to Fork for Ansible Process."),
        ),
        (
            "debug",
            ("AnsibleProcess - PID: 1: Waited, and received exit code: 0."),
        ),
        (
            "debug",
            (
                "AnsibleProcess - PID: 1: Forked process has reported no "
                "error state."
            ),
        ),
    ]

  def logs_for_main_process_with_error(self) -> List[Tuple[str, str]]:
    return [
        (
            "debug",
            ("AnsibleProcess: Preparing to Fork for Ansible Process."),
        ),
        (
            "debug",
            ("AnsibleProcess - PID: 1: Waited, and received exit code: 1."),
        ),
        (
            "error",
            (
                "AnsibleProcess - PID: 1: Forked process has reported an "
                "error state."
            ),
        ),
    ]

  def logs_for_main_process_with_interrupt(self) -> List[Tuple[str, str]]:
    return [
        (
            "debug",
            ("AnsibleProcess: Preparing to Fork for Ansible Process."),
        ),
        (
            "error",
            ("AnsibleProcess - PID: 1: Keyboard Interrupt Intercepted."),
        )
    ]

  def test_spawn_forked_process(
      self,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    split_command = shlex.split(self.command)
    m_import.side_effect = [self.mock_cli_module]
    m_os.fork.return_value = 0

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    m_os.fork.assert_called_once_with()
    self.mock_cli_class.assert_called_once_with(split_command)
    self.mock_cli_class.return_value.run.assert_called_once_with()
    self.subtest_log_content(self.logs_for_forked_process(),)

  @mock.patch(
      PROCESS_MODULE + ".sys.argv", [
          'apply',
          'github',
          'https://github.com/osx-provisioner/profile-example.git',
      ]
  )
  def test_spawn_forked_process_without_shell(
      self,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    split_command = shlex.split(self.command)
    m_import.side_effect = [self.mock_cli_module]
    m_os.fork.return_value = 0

    with self.assertRaises(SystemExit):
      self.process.spawn(self.command)

    m_os.fork.assert_called_once_with()
    self.mock_cli_class.assert_called_once_with(split_command)
    self.mock_cli_class.return_value.run.assert_called_once_with()
    self.subtest_log_content(self.logs_for_forked_process_without_shell())

  def test_spawn_forked_process_dynamic_imports(
      self,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_import.side_effect = [self.mock_cli_module]
    m_os.fork.return_value = 0

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    self.assertEqual(m_import.call_args_list, [mock.call(self.mock_module)])
    self.subtest_log_content(self.logs_for_forked_process(),)

  @mock.patch(PROCESS_MODULE + ".environment.Environment.setup")
  def test_spawn_forked_process_environment(
      self,
      m_env: mock.Mock,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_import.side_effect = [self.mock_cli_module]

    with self.assertRaises(ClickShellCleanExit):
      self.process.spawn(self.command)

    m_os.chdir.assert_called_once_with(self.process.state['profile_data_path'])
    m_env.assert_called_once_with()
    self.subtest_log_content(self.logs_for_forked_process(),)

  def test_spawn_forked_process_interrupt(
      self,
      _: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_os.chdir.side_effect = KeyboardInterrupt("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

    self.subtest_log_content(self.logs_for_forked_process()[0:2],)

  def test_spawn_forked_process_exception(
      self,
      m_import: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 0
    m_import.side_effect = [self.mock_cli_module]
    self.mock_cli_class.return_value.run.side_effect = Exception("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

    self.subtest_log_content(self.logs_for_forked_process()[0:4],)

  def test_spawn_main_process(
      self,
      _: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 0)
    m_os.WEXITSTATUS.return_value = 0

    self.process.spawn(self.command)

    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)
    self.subtest_log_content(self.logs_for_main_process_without_error())

  def test_spawn_main_process_child_error(
      self,
      _: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.return_value = (0, 256)
    m_os.WEXITSTATUS.return_value = 1

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

    m_os.fork.assert_called_once()
    m_os.waitpid.assert_called_once_with(1, 0)
    self.subtest_log_content(self.logs_for_main_process_with_error())

  def test_spawn_main_process_interrupt(
      self,
      _: mock.Mock,
      m_os: mock.Mock,
  ) -> None:
    m_os.fork.return_value = 1
    m_os.waitpid.side_effect = KeyboardInterrupt("Boom!")

    with self.assertRaises(ClickShellUncleanExit):
      self.process.spawn(self.command)

    self.subtest_log_content(self.logs_for_main_process_with_interrupt())
