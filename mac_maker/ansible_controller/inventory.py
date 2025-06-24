"""Inventory file for Ansible."""

import logging
import os

from mac_maker import config
from mac_maker.ansible_controller.interpreter import AnsibleInterpreter
from mac_maker.ansible_controller.spec import Spec
from mac_maker.utilities.mixins.text_file import TextFileWriter


class AnsibleInventoryFile(TextFileWriter):
  """Inventory file for Ansible.

  :param spec: The provisioning spec instance.
  """

  def __init__(self, spec: Spec) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.spec = spec
    self.interpreter = AnsibleInterpreter()

  def _is_already_present(self) -> bool:
    return os.path.exists(self.spec.inventory)

  def _ensure_path_exists(self) -> None:
    os.makedirs(self.spec.profile_data_path, exist_ok=True)

  def write(self) -> None:
    """Write the Ansible inventory file to the correct location."""

    if self._is_already_present():
      return

    content = config.ANSIBLE_INVENTORY_CONTENT
    content += (
        "ansible_python_interpreter=" +
        str(self.interpreter.get_interpreter_path()) + "\n"
    )

    self._ensure_path_exists()
    self.write_text_file(content, self.spec.inventory)
    self.log.debug(
        "InventoryFile: Inventory has been written to %s.",
        self.spec.inventory,
    )
