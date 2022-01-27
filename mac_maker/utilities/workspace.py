"""Workspace representation."""

import logging
from pathlib import Path
from typing import Optional

from .. import config
from .filesystem import FileSystem
from .github import GithubRepository
from .state import State


class InvalidWorkspace(Exception):
  """Raised when an improperly configured Workspace is used."""


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

    self.repository_root = (
        self.root / repo.get_zip_bundle_root_folder(branch_name)
    )
    self.log.debug(
        "WorkSpace: Attached GitHub repository to workspace: %s",
        self.repository_root,
    )

  def add_spec_file(self) -> None:
    """Generate and write a Job Spec file to this Workspace.

    :raises: :class:`InvalidWorkspace`
    """

    if not self.repository_root:
      raise InvalidWorkspace("No GitHub Repository has been added.")

    state_manager = State()
    filesystem = FileSystem(str(self.repository_root))
    spec_file_content = state_manager.state_generate(filesystem)
    state_manager.state_dehydrate(spec_file_content, filesystem.get_spec_file())
    self.spec_file = filesystem.get_spec_file()
    self.log.debug(
        "WorkSpace: Wrote Job Spec file to workspace: %s",
        filesystem.get_spec_file(),
    )
