"""Interruptable command loop for the click_shell module."""

import logging
import sys
from typing import Callable

from .. import config


class CommandLoop:
  """Command Loop with interrupt for the click_shell module."""

  interrupt_command_loop: bool = False
  exit_code: int = 0

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)

  def patch_interrupt(
      self,
      postcmd: Callable[..., bool],
  ) -> Callable[..., bool]:
    """Patch the `postcmd` method of a :class:`cmd.Cmd` instance.

    :param postcmd: The `postcmd` method of a :class:`cmd.Cmd` instance.
    :return: A patched `postcmd` method that is interruptable.
    """

    def interrupt_wrapper(*args: str, **kwargs: str) -> bool:
      if self.interrupt_command_loop:
        sys.exit(self.exit_code)
      return postcmd(*args, **kwargs)

    return interrupt_wrapper

  def exit(self, exit_code: int, pid: int) -> None:
    """Exit a process, without interrupting the command loop.

    :param exit_code: The code that will be used to exit.
    :param pid: The process ID that will be terminated.
    """

    self.log.debug(
        "CommandLoop - PID: %s: Terminating this process.",
        pid,
    )
    sys.exit(exit_code)

  def exit_shell(self, exit_code: int, pid: int) -> None:
    """Interrupt the command loop and exit the process.

    :param exit_code: The code that will be used to exit.
    :param pid: The process ID that will be terminated.
    """

    self.interrupt(exit_code, pid)
    self.exit(exit_code, pid)

  def interrupt(self, exit_code: int, pid: int) -> None:
    """Interrupt the command loop, without terminating the process.

    :param exit_code: The code that will be used to exit.
    :param pid: The process ID that will be terminated.
    """

    self.log.debug(
        (
            "CommandLoop - PID: %s: Interrupting the shell "
            "running in this process."
        ),
        pid,
    )
    self.interrupt_command_loop = True
    self.exit_code = exit_code


cmd_loop = CommandLoop()
