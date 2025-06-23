"""Ansible provisioning job spec data."""

import dataclasses
from typing import List


@dataclasses.dataclass
class Spec:
  """Ansible provisioning job spec data."""

  workspace_root_path: str
  profile_data_path: str
  galaxy_requirements_file: str
  playbook: str
  roles_path: List[str]
  collections_path: List[str]
  inventory: str
