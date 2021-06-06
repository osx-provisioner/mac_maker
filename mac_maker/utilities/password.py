"""SUDO password representation."""

import getpass
import os
import shlex
import subprocess

from .. import config
from .filesystem import FileSystem


class SUDO:
  """SUDO password representation."""

  def __init__(self, filesystem: FileSystem):
    self.filesystem = filesystem
    self.sudo_password = os.getenv(config.ENV_ANSIBLE_BECOME_PASSWORD, None)

  def prompt_for_sudo(self):
    """Prompt the user to enter the system's SUDO password."""

    if not self.sudo_password:

      while True:

        entered_password = getpass.getpass(config.SUDO_PROMPT)

        check_sudo = subprocess.Popen(
            shlex.split(config.SUDO_CHECK_COMMAND),
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        check_sudo.communicate((entered_password + '\n').encode('utf-8'))

        if not check_sudo.returncode:
          self.sudo_password = entered_password
          os.environ[config.ENV_ANSIBLE_BECOME_PASSWORD] = entered_password
          return
