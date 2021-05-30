"""SUDO password representation."""

import getpass
import os

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
      self.sudo_password = getpass.getpass(config.SUDO_PROMPT)
      os.environ[config.ENV_ANSIBLE_BECOME_PASSWORD] = self.sudo_password
