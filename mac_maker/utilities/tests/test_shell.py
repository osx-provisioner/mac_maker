"""Test the CLI Interrupt module."""

import logging
from unittest import TestCase, mock

from parameterized import parameterized_class
from ... import config
from .. import shell

SHELL_MODULE = shell.__name__


class TestCommandLoop(TestCase):
  """Test instantiating the CommandLoop class."""

  def setUp(self) -> None:
    self.instance = shell.CommandLoop()

  def test_init(self) -> None:
    self.assertFalse(self.instance.interrupt_command_loop)

    self.assertEqual(
        self.instance.exit_code,
        0,
    )


class TestCmdLoopInstance(TestCase):
  """Test the cmd_loop instance."""

  def test_is_instance_of_CommandLoop(self) -> None:
    self.assertIsInstance(shell.cmd_loop, shell.CommandLoop)


@mock.patch(SHELL_MODULE + ".sys.exit")
class TestPatchInterrupt(TestCase):
  """Test the patch_interrupt function."""

  def setUp(self) -> None:
    self.instance = shell.CommandLoop()
    self.mock_cmd_loop = mock.Mock()
    self.mock_cmd_loop.return_value = "mock_value"
    self.mock_command = "mock_command"
    self.patched_method = self.instance.patch_interrupt(self.mock_cmd_loop)

  def test__no_interrupt__zero_exit_code(
      self,
      m_exit: mock.Mock,
  ) -> None:
    self.instance.interrupt_command_loop = False
    self.instance.exit_code = 0

    result = self.patched_method(True, self.mock_command)

    self.assertEqual(
        result,
        self.mock_cmd_loop.return_value,
    )
    m_exit.assert_not_called()

  def test__interrupt__zero_exit_code(
      self,
      m_exit: mock.Mock,
  ) -> None:
    self.instance.interrupt_command_loop = True
    self.instance.exit_code = 0

    result = self.patched_method(True, self.mock_command)

    self.assertEqual(
        result,
        self.mock_cmd_loop.return_value,
    )
    m_exit.assert_called_once_with(0)

  def test__interrupt__127_exit_code(
      self,
      m_exit: mock.Mock,
  ) -> None:
    self.instance.interrupt_command_loop = True
    self.instance.exit_code = 127

    result = self.patched_method(True, self.mock_command)

    self.assertEqual(
        result,
        self.mock_cmd_loop.return_value,
    )
    m_exit.assert_called_once_with(127)


@parameterized_class(
    [
        {
            "mock_exit_code": 10,
            "mock_pid": 1000,
        },
        {
            "mock_exit_code": 127,
            "mock_pid": 2000,
        },
    ]
)
@mock.patch(SHELL_MODULE + ".sys.exit")
class TestExit(TestCase):
  """Test the exit method."""

  mock_exit_code: int
  mock_pid: int

  def setUp(self) -> None:
    self.instance = shell.CommandLoop()

  def test__exit_code(
      self,
      m_sys: mock.Mock,
  ) -> None:
    self.instance.exit(self.mock_exit_code, self.mock_pid)

    m_sys.assert_called_once_with(self.mock_exit_code)
    self.assertNotEqual(self.instance.exit_code, self.mock_exit_code)
    self.assertFalse(self.instance.interrupt_command_loop)

  def test__exit_code__logs(
      self,
      _: mock.Mock,
  ) -> None:
    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.instance.exit(self.mock_exit_code, self.mock_pid)

    self.assertEqual(
        logs.output,
        [
            (
                f'DEBUG:mac_maker:CommandLoop - PID: {self.mock_pid}: '
                'Terminating this process.'
            ),
        ],
    )


@parameterized_class(
    [
        {
            "mock_exit_code": 10,
            "mock_pid": 1000,
        },
        {
            "mock_exit_code": 127,
            "mock_pid": 2000,
        },
    ]
)
@mock.patch(SHELL_MODULE + ".sys.exit")
class TestInterrupt(TestCase):
  """Test the interrupt method."""

  mock_exit_code: int
  mock_pid: int

  def setUp(self) -> None:
    self.instance = shell.CommandLoop()

  def test__exit_code(
      self,
      m_sys: mock.Mock,
  ) -> None:
    self.instance.interrupt(self.mock_exit_code, self.mock_pid)

    m_sys.assert_not_called()
    self.assertEqual(self.instance.exit_code, self.mock_exit_code)
    self.assertTrue(self.instance.interrupt_command_loop)

  def test__exit_code_logs(
      self,
      _: mock.Mock,
  ) -> None:
    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.instance.interrupt(self.mock_exit_code, self.mock_pid)

    self.assertEqual(
        logs.output,
        [
            (
                f'DEBUG:mac_maker:CommandLoop - PID: {self.mock_pid}: '
                'Interrupting the shell running in this process.'
            ),
        ],
    )


@parameterized_class(
    [
        {
            "mock_exit_code": 10,
            "mock_pid": 1000,
        },
        {
            "mock_exit_code": 127,
            "mock_pid": 2000,
        },
    ]
)
@mock.patch(SHELL_MODULE + ".sys.exit")
class TestExitShell(TestCase):
  """Test the exit_shell method."""

  mock_exit_code: int
  mock_pid: int

  def setUp(self) -> None:
    self.instance = shell.CommandLoop()

  def test__exit_code(
      self,
      m_sys: mock.Mock,
  ) -> None:
    self.instance.exit_shell(self.mock_exit_code, self.mock_pid)

    m_sys.assert_called_once_with(self.mock_exit_code)
    self.assertEqual(self.instance.exit_code, self.mock_exit_code)
    self.assertTrue(self.instance.interrupt_command_loop)

  def test__exit_code_logs(
      self,
      _: mock.Mock,
  ) -> None:
    with self.assertLogs(config.LOGGER_NAME, logging.DEBUG) as logs:
      self.instance.exit_shell(self.mock_exit_code, self.mock_pid)

    self.assertEqual(
        logs.output,
        [
            (
                f'DEBUG:mac_maker:CommandLoop - PID: {self.mock_pid}: '
                'Interrupting the shell running in this process.'
            ),
            (
                f'DEBUG:mac_maker:CommandLoop - PID: {self.mock_pid}: '
                'Terminating this process.'
            ),
        ],
    )
