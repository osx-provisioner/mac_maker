"""Process management for Ansible commands."""

import logging
import os
import subprocess
import sys

from mac_maker import config
from mac_maker.ansible_controller import environment
from mac_maker.utilities.state import TypeState


class AnsibleProcess:
  """Process management for Ansible commands.

  :param state: The loaded runtime state object.
  """

  error_exit_code = 127

  def __init__(
      self,
      state: TypeState,
  ) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state = state

  def spawn(self, command: str) -> None:
    """Spawns an Ansible CLI Command in its own process.

    :param command: The Ansible CLI Command to spawn.
    """

    self.log.debug("AnsibleProcess: Preparing to launch Ansible Process.")
    self._call(command)

  def _call(self, command: str) -> None:
    self.log.debug(
        "AnsibleProcess: Executing '%s'",
        command,
    )

    self._environment()
    self._execution_location()

    with subprocess.Popen(
        self._normalized_command(command),
        shell=True,
    ) as worker:  # nosec B602
      self.log.debug(
          "AnsibleProcess: Spawned worker process %s",
          worker.pid,
      )

      worker.wait()

      if worker.returncode != 0:
        self.log.error("AnsibleProcess: Command failed to execute!")
        raise ChildProcessError

    self.log.debug("AnsibleProcess: Command completed successfully!")

  def _normalized_command(self, command: str) -> str:
    if getattr(sys, 'frozen', False):
      interpreter = sys.executable
      command_path = os.path.join(
          # pylint: disable=protected-access
          sys._MEIPASS,  # type: ignore[attr-defined]
          "bin",
          command,
      )
      return f'{interpreter} {command_path}'
    return command

  def _environment(self) -> None:
    env = environment.AnsibleEnvironment(self.state)
    env.setup()

  def _execution_location(self) -> None:
    os.chdir(self.state['profile_data_path'])
