"""A provisioning job for a profile in a Github repository."""

from typing import Optional, cast

import click
from .. import config
from ..utilities.github import GithubRepository
from ..utilities.precheck import TypePrecheckFileData
from ..utilities.state import TypeState
from ..utilities.workspace import WorkSpace
from . import bases


class GitHubJob(bases.JobBase):
  """A provisioning job for a profile in a Github repository.

  :param repository_url: The GitHub Repository URL.
  :param branch_name: The GitHub Repository branch name.
  """

  repository_url: str
  branch_name: Optional[str]

  def __init__(self, repository_url: str, branch_name: Optional[str]):
    super().__init__()
    self.repository_url = repository_url
    self.branch_name = branch_name

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the precheck data from a GitHub repository.

    :returns: The precheck file data.
    """

    repo = GithubRepository(self.repository_url)
    precheck_data = repo.download_zip_bundle_files(
        self.branch_name,
        {
            'notes': str(config.PRECHECK['notes']),
            'env': str(config.PRECHECK['env']),
        },
    )
    return cast(TypePrecheckFileData, precheck_data)

  def get_state(self) -> TypeState:
    """Fetch a GitHub zip bundle, and build a state object.

    :returns: The created state object.
    """

    click.echo(config.ANSIBLE_RETRIEVE_MESSAGE)

    repo = GithubRepository(self.repository_url)

    workspace = WorkSpace()
    workspace.add_repository(repo, self.branch_name)

    repo.download_zip_bundle_profile(workspace.root, self.branch_name)
    job_spec = self.jobspec.create_job_spec_from_github(workspace)

    click.echo(config.ANSIBLE_JOB_SPEC_MESSAGE)
    click.echo(job_spec['spec_file_location'])
    return job_spec['spec_file_content']
