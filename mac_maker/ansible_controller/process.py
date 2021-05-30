"""Process management for Ansible commands."""

import logging
import os
import shlex
from typing import Type, Union

from ansible.cli import CLI
from ansible.utils.display import initialize_locale
from click_shell.exceptions import ClickShellCleanExit, ClickShellUncleanExit
from .. import config


class AnsibleProcess:
  """Process management for Ansible commands."""

  def __init__(self, ansible_cli_class: Type[CLI], state: dict):
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state = state
    self.ansible_cli_class = ansible_cli_class
    self.pid: Union[None, int] = None

  def spawn(self, command: str):
    """Spawns an Ansible CLI Command in it's own process.

    :param command: The Ansible CLI Command to spawn.
    """

    self.log.debug("AnsibleProcess: Preparing to Fork for Ansible Process")
    self.pid = os.fork()
    if self.pid == 0:
      self._forked_process(command)
    else:
      self._main_process()

  def _execution_location(self):
    os.chdir(self.state['profile_data_path'])

  def _environment(self):
    initialize_locale()
    roles_paths_string = ":".join(self.state['roles_path'])
    os.environ[config.ENV_ANSIBLE_ROLES_PATH] = roles_paths_string

  def _forked_process(self, command: str):
    try:
      self.log.debug(
          "AnsibleProcess: Forked process is now executing: %s",
          command,
      )

      self._environment()
      self._execution_location()

      instance = self.ansible_cli_class(shlex.split(command))
      try:
        instance.run()
      except Exception:
        raise ClickShellUncleanExit()  # pylint: disable=raise-missing-from
      raise ClickShellCleanExit()
    except KeyboardInterrupt:
      self.log.error("AnsibleProcess: Keyboard Interrupt Intercepted.")
      raise ClickShellUncleanExit() from KeyboardInterrupt

  def _main_process(self):
    try:
      os.waitpid(self.pid, 0)
      self.log.debug("AnsibleProcess: Forked process has completed.")
    except KeyboardInterrupt:
      self.log.error("AnsibleProcess: Keyboard Interrupt Intercepted.")
      raise ClickShellUncleanExit() from KeyboardInterrupt
