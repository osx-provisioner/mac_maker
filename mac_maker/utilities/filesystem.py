"""File system representation."""

from pathlib import Path

from .. import config
from .decorators import convertable_path


class FileSystem:
  """File system representation."""

  def __init__(
      self,
      work_space_root: str,
  ):
    self.work_space_root = Path(work_space_root)

  @convertable_path
  def get_work_space_root(self) -> Path:
    """Returns the work space's root folder location."""
    return self.work_space_root

  @convertable_path
  def get_spec_file(self) -> Path:
    """Returns the current spec file's location."""
    return self.work_space_root / config.STATE_FILE_NAME

  @convertable_path
  def get_inventory_file(self) -> Path:
    """Returns the Ansible inventory file's location."""
    return self.get_profile_data_path() / config.PROFILE_INVENTORY_FILE

  @convertable_path
  def get_galaxy_requirements_file(self) -> Path:
    """Returns the Ansible Galaxy requirements file's location."""
    return (
        self.get_profile_data_path() / config.PROFILE_GALAXY_REQUIREMENTS_FILE
    )

  @convertable_path
  def get_playbook_file(self) -> Path:
    """Returns the main Ansible Playbook file's location."""
    return self.get_profile_data_path() / config.PROFILE_INSTALLER_FILE

  @convertable_path
  def get_profile_data_path(self) -> Path:
    """Returns the current profile's root folder location."""
    return self.work_space_root / config.PROFILE_FOLDER_PATH

  @convertable_path
  def get_roles_path(self) -> Path:
    """Returns the current Ansible roles folder location(s)."""
    return self.get_profile_data_path() / "roles"

  @convertable_path
  def get_collections_path(self) -> Path:
    """Returns the current Ansible collections folder location(s)."""
    return self.get_profile_data_path() / "collections"
