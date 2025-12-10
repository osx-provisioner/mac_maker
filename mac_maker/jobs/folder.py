"""A provisioning job for a Profile in a file system folder."""

from typing import Optional

import click
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.utilities.workspace import WorkSpace


class FolderJob(ProvisionerJobBase):
  """A provisioning job for a Profile in a file system folder.

  :param folder_path: The local file system folder path containing a profile.
  """

  folder_path: str
  workspace: Optional[WorkSpace]

  class Messages(ProvisionerJobBase.Messages):
    load_folder_profile = "--- Loading Folder Profile ---"

  def __init__(self, folder_path: str):
    super().__init__()
    self.folder_path = folder_path
    self.workspace = None

  def initialize_spec_file(self) -> None:
    """Initialize the spec file for this provisioning job."""

    click.echo(self.Messages.load_folder_profile)

    self.workspace = WorkSpace()
    self.workspace.add_folder(self.folder_path)
    self.workspace.add_spec_file()
    self.spec_file.path = str(self.workspace.spec_file)
    self.spec_file.load()
