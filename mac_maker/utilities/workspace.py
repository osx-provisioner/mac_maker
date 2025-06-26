"""Workspace representation."""

import logging
from pathlib import Path
from typing import Optional

from mac_maker import config
from mac_maker.ansible_controller.spec import Spec
from mac_maker.profile import Profile, spec_file
from mac_maker.utilities.exceptions import WorkSpaceInvalid
from mac_maker.utilities.github import GithubRepository


class WorkSpace:
  """Workspace representation."""

  class Messages:
    add_repository = "WorkSpace: Attached GitHub repository to workspace: %s."
    add_spec_file = "WorkSpace: Wrote spec file to workspace: %s."
    error_no_repository = "No GitHub Repository has been added."

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.root = Path(config.WORKSPACE).resolve()
    self.repository_root: Optional[Path] = None
    self.spec_file: Optional[Path] = None

  def add_repository(
      self,
      repo: GithubRepository,
      branch_name: Optional[str],
  ) -> None:
    """Add a GitHub Repository to the current Workspace.

    :param repo: The GitHub Repository object.
    :param branch_name: The GitHub Repository branch name.
    """

    repo.download_zip_bundle_profile(self.root, branch_name)
    self.repository_root = (
        self.root / repo.get_zip_bundle_root_folder(branch_name)
    )
    self.log.debug(
        self.Messages.add_repository,
        self.repository_root,
    )

  def add_spec_file(self) -> None:
    """Generate and write a spec file to this workspace.

    :raises: :class:`WorkSpaceInvalid`
    """

    if not self.repository_root:
      raise WorkSpaceInvalid(self.Messages.error_no_repository)

    profile_instance = Profile(str(self.repository_root))
    spec_file_instance = spec_file.SpecFile()
    spec_file_instance.path = profile_instance.get_spec_file()
    spec_file_instance.content = Spec.from_profile(profile_instance)
    spec_file_instance.write()
    self.log.debug(
        self.Messages.add_spec_file,
        self.spec_file,
    )
