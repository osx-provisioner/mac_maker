"""Workspace representation."""

import logging
import os
import shutil
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
    add_folder = "WorkSpace: Copied local folder to workspace: %s."
    add_repository = "WorkSpace: Attached GitHub repository to workspace: %s."
    add_spec_file = "WorkSpace: Attached spec file to workspace: %s."
    error_no_repository = "No GitHub Repository has been added."
    error_not_a_folder = "The location '%s' is not a directory!"
    error_profile_copy_failure = (
        "Unable to copy content from target location '%s'!"
    )

  def __init__(self) -> None:
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.profile_root: Optional[Path] = None
    self.root = Path(config.WORKSPACE).resolve()
    self.spec_file: Optional[Path] = None
    self._reset()

  def add_folder(
      self,
      folder_location: str,
  ) -> None:
    """Add a local filesystem folder to the current Workspace.

    :param folder_location: A validated filesystem path to add.
    """

    profile_basename = os.path.basename(folder_location)

    try:
      shutil.copytree(
          folder_location,
          self.root / profile_basename,
      )
    except Exception as exc:
      raise IOError(
          self.Messages.error_profile_copy_failure % folder_location
      ) from exc

    self.profile_root = self.root / profile_basename
    self.log.debug(
        self.Messages.add_folder,
        self.profile_root,
    )

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
    self.profile_root = (
        self.root / repo.get_zip_bundle_root_folder(branch_name)
    )
    self.log.debug(
        self.Messages.add_repository,
        self.profile_root,
    )

  def add_spec_file(self) -> None:
    """Generate and write a spec file to this workspace.

    :raises: :class:`WorkSpaceInvalid`
    """

    if not self.profile_root:
      raise WorkSpaceInvalid(self.Messages.error_no_repository)

    profile_instance = Profile(str(self.profile_root))
    spec_file_instance = spec_file.SpecFile()
    spec_file_instance.path = profile_instance.get_spec_file()
    spec_file_instance.content = Spec.from_profile(profile_instance)
    spec_file_instance.write()

    self.log.debug(
        self.Messages.add_spec_file,
        spec_file_instance.path,
    )

    self.spec_file = spec_file_instance.path

  def _reset(self) -> None:
    """If a workspace already exists at the given path, then remove it."""

    if os.path.exists(self.root):
      shutil.rmtree(self.root)

    os.mkdir(self.root)
