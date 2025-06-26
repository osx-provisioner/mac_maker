"""Runtime state for the Ansible Runner."""

import logging
from pathlib import Path
from typing import List, TypedDict, Union, cast

from mac_maker import config
from mac_maker.utilities.filesystem import FileSystem
from mac_maker.utilities.mixins.json_file import JSONFileReader, JSONFileWriter


class TypeState(TypedDict):
  """Typed representation of the Ansible Runner's runtime state."""

  workspace_root_path: str
  profile_data_path: str
  galaxy_requirements_file: str
  playbook: str
  roles_path: List[str]
  collections_path: List[str]
  inventory: str


class State(JSONFileReader, JSONFileWriter):
  """Runtime state persistence and generation for the Ansible Runner."""

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)

  def state_generate(self, filesystem: FileSystem) -> TypeState:
    """Generate a new runtime state object from a FileSystem instance.

    :param filesystem: The FileSystem object you are using.
    :returns: The generated runtime state object.
    """
    self.log.debug("State: Generating new Ansible runtime state.")
    return TypeState(
        workspace_root_path=str(filesystem.get_work_space_root().resolve()),
        profile_data_path=str(filesystem.get_profile_data_path().resolve()),
        galaxy_requirements_file=str(
            filesystem.get_galaxy_requirements_file().resolve()
        ),
        playbook=str(filesystem.get_playbook_file().resolve()),
        roles_path=[str(filesystem.get_roles_path().resolve())],
        collections_path=[str(filesystem.get_collections_path().resolve())],
        inventory=str(filesystem.get_inventory_file().resolve()),
    )

  def state_dehydrate(
      self, state_data: TypeState, spec_file_path: Union[Path, str]
  ) -> None:
    """Write a runtime state object to a Job Spec file.

    :param state_data: The Python object that represents the runtime state.
    :param spec_file_path: The path to the Job Spec file that will be written.
    """
    self.log.debug("State: saving runtime state as a Job Spec file.")
    self.write_json_file(state_data, spec_file_path)

  def state_rehydrate(self, spec_file_path: Union[Path, str]) -> TypeState:
    """Read a runtime state object from a Job Spec file.

    :param spec_file_path: The path to the Job Spec file that will be read.
    :returns: The runtime state object.
    """

    self.log.debug("State: loading runtime state from Job Spec file.")
    state_data = self.load_json_file(spec_file_path)
    return cast(TypeState, state_data)
