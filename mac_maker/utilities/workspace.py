"""Workspace representation."""

import logging
from pathlib import Path
from typing import Optional

from mac_maker import config
from mac_maker.profile import Profile
from mac_maker.utilities.exceptions import WorkSpaceInvalid
from mac_maker.utilities.github import GithubRepository
from mac_maker.utilities.state import State


class WorkSpace:
  """Workspace representation."""

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
        "WorkSpace: Attached GitHub repository to workspace: %s.",
        self.repository_root,
    )

  def add_spec_file(self) -> None:
    """Generate and write a spec file to this workspace.

    :raises: :class:`InvalidWorkspace`
    """

    if not self.repository_root:
      raise WorkSpaceInvalid("No GitHub Repository has been added.")

    state_manager = State()
    profile = Profile(str(self.repository_root))
    self.spec_file = profile.get_spec_file()
    spec_file_content = state_manager.state_generate(profile)
    state_manager.state_dehydrate(spec_file_content, self.spec_file)
    self.log.debug(
        "WorkSpace: Wrote spec file to workspace: %s.",
        self.spec_file,
    )
