"""Inventory file for Ansible."""

import logging
import os

from .. import config


class InventoryFile:
  """Inventory file for Ansible."""

  def __init__(self, spec: dict):
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.spec = spec

  def _is_already_present(self):
    return os.path.exists(self.spec['inventory'])

  def _ensure_path_exists(self):
    os.makedirs(self.spec['profile_data_path'], exist_ok=True)

  def write_inventory_file(self):
    """Write the Ansible inventory file to the correct location."""

    if self._is_already_present():
      return

    self._ensure_path_exists()

    with open(self.spec['inventory'], "w", encoding="utf-8") as fhandle:
      fhandle.write(config.ANSIBLE_INVENTORY_CONTENT)
    self.log.debug(
        "InventoryFile: inventory has been written to %s",
        self.spec['inventory'],
    )
