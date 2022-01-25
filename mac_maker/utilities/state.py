"""State for the Ansible Runner."""

import logging
from pathlib import Path
from typing import List, TypedDict, Union, cast

from .. import config
from .filesystem import FileSystem
from .mixins.json_file import JSONFileReader, JSONFileWriter


class TypeState(TypedDict):
  """Typed representation of a state file."""

  workspace_root_path: str
  profile_data_path: str
  galaxy_requirements_file: str
  playbook: str
  roles_path: List[str]
  collections_path: List[str]
  inventory: str


class State(JSONFileReader, JSONFileWriter):
  """State persistence and generation for the Ansible Runner."""

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)

  def state_generate(self, filesystem: FileSystem) -> TypeState:
    """Generate a new state object from a FileSystem instance.

    :param filesystem: The FileSystem object you are using.
    :returns: The generated state content.
    """
    self.log.debug("State: Generating New Ansible State Content")
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
    """Write a state object to a spec file.

    :param state_data: The Python dictionary that represents the state.
    :param spec_file_path: The path to the state file that will be written.
    :returns: The state object.
    """
    self.log.debug("State: saving State as Spec File")
    self.write_json_file(state_data, spec_file_path)

  def state_rehydrate(self, spec_file_path: Union[Path, str]) -> TypeState:
    """Read a state object from a spec file.

    :param spec_file_path: The path to the state file that will be read.
    :returns: The state object.
    """

    self.log.debug("State: loading State from Spec File")
    state_data = self.load_json_file(spec_file_path)
    return cast(TypeState, state_data)
