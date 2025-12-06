"""A provisioning job for a Profile on the local file system."""

from typing import Optional

import click
from mac_maker import config
from mac_maker.ansible_controller.spec import Spec
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.utilities.github import GithubRepository
from mac_maker.utilities.workspace import WorkSpace


class FolderJob(ProvisionerJobBase):
  """A provisioning job for a Profile on the local file system.

  :param folder_location: The filesystem path containing a valid profile.
  """

  folder_location: str
  workspace: Optional[WorkSpace]

  class Messages:
    copy_profile_content = "Copying profile from the specified filesystem location ..."

  def __init__(self, folder_location: str):
    super().__init__()
    self.folder_location = folder_location
    self.workspace = None

  def _initialize_workspace(self) -> None:
    if self.workspace:
      return

    click.echo(self.Messages.copy_profile_content)

    self.workspace = WorkSpace()
    self.workspace.add_folder(self.folder_location)
    self.workspace.add_spec_file()
    self.spec_file.path = str(self.workspace.spec_file)
    self.spec_file.load()

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the Precheck data from a GitHub Repository.

    :returns: The Precheck file data.
    """

    # TODO: extract basecase from this

    self._initialize_workspace()
    precheck_data = self.precheck_extractor.get_precheck_data(
        self.spec_file.content
    )
    return precheck_data

  def get_spec(self) -> Spec:
    """Assemble and return a provisioning spec instance.

    :returns: The created provisioning spec instance.
    """

    # TODO: extract basecase from this

    self._initialize_workspace()
    click.echo(config.SPEC_FILE_CREATED_MESSAGE)
    click.echo(self.spec_file.path)
    return self.spec_file.content
