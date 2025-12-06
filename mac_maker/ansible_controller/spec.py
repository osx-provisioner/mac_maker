"""Ansible provisioning job spec data."""

import dataclasses
from typing import List

from mac_maker.profile import Profile


@dataclasses.dataclass
class Spec:
  """Ansible provisioning job spec."""

  workspace_root_path: str
  profile_data_path: str
  galaxy_requirements_file: str
  playbook: str
  roles_path: List[str]
  collections_path: List[str]
  inventory: str

  @classmethod
  def from_profile(cls, profile: Profile) -> "Spec":
    """Generate a provisioning spec from a profile instance.

    :param profile: The profile being used.
    :returns: The created spec instance.
    """

    return cls(
        workspace_root_path=str(profile.get_profile_root().resolve()),
        profile_data_path=str(profile.get_profile_data_path().resolve()),
        galaxy_requirements_file=str(
            profile.get_galaxy_requirements_file().resolve()
        ),
        playbook=str(profile.get_playbook_file().resolve()),
        roles_path=[str(profile.get_roles_path().resolve())],
        collections_path=[str(profile.get_collections_path().resolve())],
        inventory=str(profile.get_inventory_file().resolve()),
    )
