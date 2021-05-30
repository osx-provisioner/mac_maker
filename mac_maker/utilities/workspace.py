"""Workspace representation."""

import logging
import tempfile
from pathlib import Path
from typing import Union

from .. import config
from .github import GithubRepository


class WorkSpace:
  """Workspace representation."""

  def __init__(self):
    self.tmp = tempfile.gettempdir()
    self.root = Path(config.WORKSPACE).resolve()
    self.repository_root = None
    self.log = logging.getLogger(config.LOGGER_NAME)

  def add_repository(
      self,
      repo: GithubRepository,
      branch_name: Union[None, str],
  ):
    """Add a GitHub repository to the current workspace.

    :param repo: The GitHub Repository Object
    :param branch_name: The GitHub Repository branch name
    """

    self.repository_root = (
        self.root / repo.get_zip_bundle_root_folder(branch_name)
    )
    self.log.debug(
        "WorkSpace: Attached GitHub repository to workspace: %s",
        self.repository_root,
    )
