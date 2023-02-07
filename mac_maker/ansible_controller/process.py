"""Process management for Ansible commands."""

import importlib
import logging
import os
import shlex
import traceback

import click
from .. import config
from ..utilities.shell import cmd_loop
from ..utilities.state import TypeState
from . import environment


class AnsibleProcess:
  """Process management for Ansible commands.

  :param ansible_module: Dot path of the ansible module to load.
  :param ansible_class: The Ansible class to import from this module.
  :param state: The loaded runtime state object.
  """

  error_exit_code = 127

  def __init__(
      self, ansible_module: str, ansible_class: str, state: TypeState
  ) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state = state
    self.ansible_class = ansible_class
    self.ansible_module = ansible_module

  def spawn(self, command: str) -> None:
    """Spawns an Ansible CLI Command in it's own process.

    :param command: The Ansible CLI Command to spawn.
    """

    self.log.debug("AnsibleProcess: Preparing to Fork for Ansible Process.")
    pid = os.fork()
    if pid == 0:
      self._forked_process(command, pid)
    else:
      self._main_process(command, pid)

  def _forked_process(self, command: str, pid: int) -> None:
    try:
      self.log.debug(
          "AnsibleProcess - PID: %s: Forked process is now executing: %s.",
          pid,
          command,
      )

      self._environment()
      self._execution_location()

      ansible_cli_module = importlib.import_module(self.ansible_module)
      ansible_cli_class = getattr(ansible_cli_module, self.ansible_class)

      instance = ansible_cli_class(shlex.split(command))

      self.log.debug(
          (
              "AnsibleProcess - PID: %s: Forked process Ansible CLI Class "
              "instance has been created: %s."
          ),
          pid,
          str(instance),
      )

      try:
        self.log.debug(
            (
                "AnsibleProcess - PID: %s: Forked process Ansible CLI Class "
                "instance is calling run."
            ),
            pid,
        )
        instance.run()
        self.log.debug(
            "AnsibleProcess - PID: %s: Forked process has finished.",
            pid,
        )
        cmd_loop.exit_shell(0, pid)
      except Exception:  # pylint: disable=broad-exception-caught
        traceback.print_exc()
        cmd_loop.exit_shell(self.error_exit_code, pid)
    except KeyboardInterrupt:
      cmd_loop.exit_shell(self.error_exit_code, pid)

  def _environment(self) -> None:
    env = environment.Environment(self.state)
    env.setup()

  def _execution_location(self) -> None:
    os.chdir(self.state['profile_data_path'])

  def _main_process(self, command: str, pid: int) -> None:
    try:
      _, exit_status = os.waitpid(pid, 0)
      status_code = os.WEXITSTATUS(exit_status)
      self.log.debug(
          "AnsibleProcess - PID: %s: Waited, and received exit code: %s.",
          pid,
          status_code,
      )
      if status_code:
        click.echo("ANSIBLE ERROR: Non zero exit code.")
        click.echo(f"COMMAND: {command}")
        self.log.error(
            (
                "AnsibleProcess - PID: %s: Forked process has reported an "
                "error state."
            ),
            pid,
        )
        cmd_loop.exit(status_code, pid)
      else:
        self.log.debug(
            (
                "AnsibleProcess - PID: %s: Forked process has reported no "
                "error state."
            ),
            pid,
        )
    except KeyboardInterrupt:
      self.log.error(
          "AnsibleProcess - PID: %s: Keyboard Interrupt Intercepted.",
          pid,
      )
      cmd_loop.exit(self.error_exit_code, pid)
