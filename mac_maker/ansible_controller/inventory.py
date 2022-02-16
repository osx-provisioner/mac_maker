"""Inventory file for Ansible."""

import logging
import os

from .. import config
from ..utilities.mixins.text_file import TextFileWriter
from ..utilities.state import TypeState


class InventoryFile(TextFileWriter):
  """Inventory file for Ansible.

  :param state: The loaded runtime state object.
  """

  def __init__(self, state: TypeState) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.state = state

  def _is_already_present(self) -> bool:
    return os.path.exists(self.state['inventory'])

  def _ensure_path_exists(self) -> None:
    os.makedirs(self.state['profile_data_path'], exist_ok=True)

  def write_inventory_file(self) -> None:
    """Write the Ansible inventory file to the correct location."""

    if self._is_already_present():
      return

    self._ensure_path_exists()
    self.write_text_file(
        config.ANSIBLE_INVENTORY_CONTENT, self.state['inventory']
    )
    self.log.debug(
        "InventoryFile: Inventory has been written to %s.",
        self.state['inventory'],
    )
