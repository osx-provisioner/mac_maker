"""A provisioning job for a Profile in a GitHub Repository."""

from typing import Optional

import click
from mac_maker import config
from mac_maker.ansible_controller.spec import Spec
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.utilities.github import GithubRepository
from mac_maker.utilities.workspace import WorkSpace


class GitHubJob(ProvisionerJobBase):
  """A provisioning job for a Profile in a GitHub Repository.

  :param repository_url: The GitHub Repository URL.
  :param branch_name: The GitHub Repository branch name.
  """

  repository_url: str
  branch_name: Optional[str]
  workspace: Optional[WorkSpace]

  def __init__(self, repository_url: str, branch_name: Optional[str]):
    super().__init__()
    self.branch_name = branch_name
    self.repository = GithubRepository(repository_url)
    self.workspace = None

  def _initialize_workspace(self) -> None:
    if self.workspace:
      return

    click.echo(config.ANSIBLE_RETRIEVE_MESSAGE)

    self.workspace = WorkSpace()
    self.workspace.add_repository(self.repository, self.branch_name)
    self.workspace.add_spec_file()
    self.spec_file.path = str(self.workspace.spec_file)
    self.spec_file.load()

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the Precheck data from a GitHub Repository.

    :returns: The Precheck file data.
    """

    self._initialize_workspace()
    precheck_data = self.precheck_extractor.get_precheck_data(
        self.spec_file.content
    )
    return precheck_data

  def get_spec(self) -> Spec:
    """Assemble and return a provisioning spec instance.

    :returns: The created provisioning spec instance.
    """

    self._initialize_workspace()
    click.echo(config.SPEC_FILE_CREATED_MESSAGE)
    click.echo(self.spec_file.path)
    return self.spec_file.content
