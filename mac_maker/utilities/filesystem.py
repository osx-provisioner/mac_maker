"""File system representation."""

from pathlib import Path
from typing import Union, cast

from .. import config
from .decorators import convertible_path


class FileSystem:
  """File system representation.

  :param work_space_root: The path of the work space root location.
  """

  def __init__(
      self,
      work_space_root: Union[Path, str],
  ) -> None:
    self.work_space_root = Path(work_space_root)

  @convertible_path
  def get_work_space_root(self) -> Path:
    """Return the work space's root folder location.

    :return: The work space's root folder location.
    """
    return self.work_space_root

  @convertible_path
  def get_spec_file(self) -> Path:
    """Return the current spec file's location.

    :return: The current spec file's location.
    """
    return self.work_space_root / config.STATE_FILE_NAME

  @convertible_path
  def get_inventory_file(self) -> Path:
    """Return the Ansible inventory file's location.

    :return: The Ansible inventory file's location.
    """
    return cast(
        Path, self.get_profile_data_path()
    ) / config.PROFILE_INVENTORY_FILE

  @convertible_path
  def get_galaxy_requirements_file(self) -> Path:
    """Return the Ansible Galaxy requirements file's location.

    :return: The Ansible Galaxy requirements file's location.
    """
    return (
        cast(Path, self.get_profile_data_path()) /
        config.PROFILE_GALAXY_REQUIREMENTS_FILE
    )

  @convertible_path
  def get_playbook_file(self) -> Path:
    """Return the main Ansible Playbook file's location.

    :return: The main Ansible Playbook file's location.
    """
    return cast(
        Path, self.get_profile_data_path()
    ) / config.PROFILE_INSTALLER_FILE

  @convertible_path
  def get_profile_data_path(self) -> Path:
    """Return the Mac Maker profile's root folder location.

    :return: The Mac Maker profile's root folder location.
    """
    return self.work_space_root / config.PROFILE_FOLDER_PATH

  @convertible_path
  def get_roles_path(self) -> Path:
    """Return the Ansible roles folder's location(s).

    :return: The Ansible roles folder's location(s).
    """
    return cast(Path, self.get_profile_data_path()) / "roles"

  @convertible_path
  def get_collections_path(self) -> Path:
    """Return the Ansible collections folder's location(s).

    :return: The Ansible collections folder's location(s).
    """
    return cast(Path, self.get_profile_data_path()) / "collections"
