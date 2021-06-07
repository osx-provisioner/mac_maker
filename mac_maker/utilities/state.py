"""State for the Ansible Runner."""

import json
import logging
from pathlib import Path

from .. import config
from .filesystem import FileSystem


class State:
  """State for the Ansible Runner."""

  def __init__(self):
    self.log = logging.getLogger(config.LOGGER_NAME)

  def state_generate(self, filesystem: FileSystem):
    """Generate a new state file from a FileSystem instance.

    :param filesystem: The FileSystem object you are using.
    """

    self.log.debug("State: Generating New Ansible State Content")
    return {
        "workspace_root_path":
            filesystem.get_work_space_root(string=True),
        "profile_data_path":
            filesystem.get_profile_data_path(string=True),
        "galaxy_requirements_file":
            filesystem.get_galaxy_requirements_file(string=True),
        "playbook":
            filesystem.get_playbook_file(string=True),
        "roles_path": [filesystem.get_roles_path(string=True)],
        "collections_path": [filesystem.get_collections_path(string=True)],
        "inventory":
            filesystem.get_inventory_file(string=True),
    }

  def state_dehydrate(self, state_data: dict, state_filename: Path) -> dict:
    """Write a state file to disk.

    :param state_data: The Python dictionary that represents the state.
    :param state_filename: The path to the state file that will be written.
    """

    self.log.debug("State: saving State as Spec File")
    with open(state_filename, "w") as file_handle:
      json.dump(state_data, file_handle)
    return state_data

  def state_rehydrate(self, state_filename: Path) -> dict:
    """Write a state file to disk.

    :param state_filename: The path to the state file that will be read.
    """

    self.log.debug("State: Loading State from Spec File")
    with open(state_filename) as file_handle:
      state_data = json.load(file_handle)
    return state_data
