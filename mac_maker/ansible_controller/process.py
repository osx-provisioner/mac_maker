"""Process management for Ansible commands."""

import importlib
import logging
import os
import shlex
import sys
import traceback

import click
from click_shell.exceptions import ClickShellCleanExit, ClickShellUncleanExit
from .. import cli, config
from ..utilities.state import TypeState
from . import environment


class AnsibleProcess:
  """Process management for Ansible commands.

  :param ansible_module: Dot path of the ansible module to load.
  :param ansible_class: The ansible class to import from the module.
  :param state: The loaded run time state.
  """

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

    self.log.debug("AnsibleProcess: Preparing to Fork for Ansible Process")
    pid = os.fork()
    if pid == 0:
      self._forked_process(command)
    else:
      self._main_process(command, pid)

  def _forked_process(self, command: str) -> None:
    try:
      self.log.debug(
          "AnsibleProcess: Forked process is now executing: %s",
          command,
      )

      self._environment()
      self._execution_location()

      ansible_cli_module = importlib.import_module(self.ansible_module)
      ansible_cli_class = getattr(ansible_cli_module, self.ansible_class)

      instance = ansible_cli_class(shlex.split(command))

      try:
        instance.run()
      except Exception:
        traceback.print_exc()
        raise ClickShellUncleanExit()  # pylint: disable=raise-missing-from
      self._perform_clean_exit()
    except KeyboardInterrupt:
      self.log.error("AnsibleProcess: Keyboard Interrupt Intercepted.")
      raise ClickShellUncleanExit() from KeyboardInterrupt

  def _environment(self) -> None:
    display = importlib.import_module(config.ANSIBLE_LIBRARY_LOCALE_MODULE)
    display.initialize_locale()  # type: ignore[attr-defined]
    env = environment.Environment(self.state)
    env.setup()

  def _execution_location(self) -> None:
    os.chdir(self.state['profile_data_path'])

  def _main_process(self, command: str, pid: int) -> None:
    try:
      _, exit_status = os.waitpid(pid, 0)
      if os.WEXITSTATUS(exit_status):
        click.echo("ANSIBLE ERROR: Non zero exit code.")
        click.echo(f"COMMAND: {command}")
        self.log.error("AnsibleProcess: Forked process reports error.")
        raise ClickShellUncleanExit()
      self.log.debug("AnsibleProcess: Forked process has completed.")
    except KeyboardInterrupt:
      self.log.error("AnsibleProcess: Keyboard Interrupt Intercepted.")
      raise ClickShellUncleanExit() from KeyboardInterrupt

  def _perform_clean_exit(self) -> None:
    if self._was_started_without_shell():
      sys.exit(0)
    raise ClickShellCleanExit()

  # TODO: Move into CLI module?
  def _was_started_without_shell(self) -> bool:
    for command in cli.cli.commands.keys():
      if command in sys.argv:
        return True
    return False
