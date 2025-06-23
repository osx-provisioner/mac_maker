"""Mac Maker Profile."""

from pathlib import Path
from typing import Union

from mac_maker import config


class Profile:
  """Mac Maker Profile.

  :param profile_root: The path of the Profile's root location.
  """

  def __init__(
      self,
      profile_root: Union[Path, str],
  ) -> None:
    self.profile_root = Path(profile_root)

  def get_profile_root(self) -> Path:
    """Return the Profile's root folder location.

    :return: The Profile's root folder location.
    """
    return self.profile_root

  def get_spec_file(self) -> Path:
    """Return the spec file's location.

    :return: The spec file's location.
    """
    return self.profile_root / config.SPEC_FILE_NAME

  def get_inventory_file(self) -> Path:
    """Return the Ansible inventory file's location.

    :return: The Ansible inventory file's location.
    """
    return self.get_profile_data_path() / config.PROFILE_INVENTORY_FILE

  def get_galaxy_requirements_file(self) -> Path:
    """Return the Ansible Galaxy requirements file's location.

    :return: The Ansible Galaxy requirements file's location.
    """
    return self.get_profile_data_path(
    ) / config.PROFILE_GALAXY_REQUIREMENTS_FILE

  def get_playbook_file(self) -> Path:
    """Return the main Ansible playbook file's location.

    :return: The main Ansible playbook file's location.
    """
    return self.get_profile_data_path() / config.PROFILE_INSTALLER_FILE

  def get_profile_data_path(self) -> Path:
    """Return the Mac Maker profile's root folder location.

    :return: The Mac Maker profile's root folder location.
    """
    return self.profile_root / config.PROFILE_FOLDER_PATH

  def get_roles_path(self) -> Path:
    """Return the Ansible roles folder's location(s).

    :return: The Ansible roles folder's location(s).
    """
    return self.get_profile_data_path() / "roles"

  def get_collections_path(self) -> Path:
    """Return the Ansible collections folder's location(s).

    :return: The Ansible collections folder's location(s).
    """
    return self.get_profile_data_path() / "collections"
