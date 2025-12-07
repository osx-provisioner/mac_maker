"""A provisioning job for a Profile in a GitHub Repository."""

from typing import Optional

import click
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.utilities.github import GithubRepository
from mac_maker.utilities.workspace import WorkSpace


class GitHubJob(ProvisionerJobBase):
  """A provisioning job for a Profile in a GitHub Repository.

  :param repository_url: The GitHub Repository URL.
  :param branch_name: The GitHub Repository branch name.
  """

  branch_name: Optional[str]
  repository_url: str
  workspace: Optional[WorkSpace]

  class Messages(ProvisionerJobBase.Messages):
    retrieve_github_profile = "--- Retrieving Remote Profile ---"

  def __init__(self, repository_url: str, branch_name: Optional[str]):
    super().__init__()
    self.branch_name = branch_name
    self.repository = GithubRepository(repository_url)
    self.workspace = None

  def initialize_spec_file(self) -> None:
    """Initialize the spec file for this provisioning job."""

    click.echo(self.Messages.retrieve_github_profile)

    self.workspace = WorkSpace()
    self.workspace.add_repository(self.repository, self.branch_name)
    self.workspace.add_spec_file()
    self.spec_file.path = str(self.workspace.spec_file)
    self.spec_file.load()
