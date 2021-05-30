"""Jobs for the Mac Maker."""

import sys
from typing import Dict, Union

import click
import pkg_resources
from . import config
from .ansible_controller.inventory import InventoryFile
from .ansible_controller.runner import AnsibleRunner
from .utilities.filesystem import FileSystem
from .utilities.github import GithubRepository
from .utilities.password import SUDO
from .utilities.precheck import PrecheckConfig
from .utilities.spec import JobSpec
from .utilities.workspace import WorkSpace


class Jobs:
  """Jobs for the Mac Maker."""

  def __init__(self,):
    self.jobspec = JobSpec()

  def get_precheck_content_from_github(
      self, repository_url: str, branch_name: Union[None, str]
  ) -> Dict[str, str]:
    """Read the precheck data from a GitHub repository.

    :param repository_url: The GitHub Repository URL.
    :param branch_name: The GitHub Repository branch name.
    """

    repo = GithubRepository(repository_url)
    profile_data = repo.download_zip_bundle_files(
        branch_name,
        {
            'notes': str(config.PRECHECK['notes']),
            'env': str(config.PRECHECK['env']),
        },
    )
    return profile_data

  def get_precheck_content_from_spec(
      self,
      spec_file_location: str,
  ) -> Dict[str, str]:
    """Read the precheck data using a spec file."""

    precheck_data = self.jobspec.extract_precheck_from_job_spec(
        spec_file_location
    )
    return precheck_data

  def precheck(self, precheck_data: Dict[str, str]):
    """Precheck the profile for validity and environment variable content."""

    validator = PrecheckConfig(precheck_data['env'])
    validator.is_valid_env_file()
    results = validator.validate_environment()
    if not results['is_valid']:
      for violation in results['violations']:
        click.echo(violation)
      sys.exit(1)
    click.echo(precheck_data['notes'])

  def create_spec_from_github(
      self, repository_url: str, branch_name: Union[None, str]
  ) -> dict:
    """Fetch a GitHub zip bundle, and build a spec file.

    :param repository_url: The GitHub Repository URL.
    :param branch_name: The GitHub Repository branch name.
    """

    click.echo(config.ANSIBLE_RETRIEVE_MESSAGE)

    repo = GithubRepository(repository_url)

    workspace = WorkSpace()
    workspace.add_repository(repo, branch_name)

    repo.download_zip_bundle_profile(workspace.root, branch_name)
    job_spec = self.jobspec.create_job_spec_from_github(workspace)

    click.echo(config.ANSIBLE_JOB_SPEC_MESSAGE)
    click.echo(job_spec['spec_file_location'])
    return job_spec['spec_file_content']

  def create_spec_from_spec_file(self, spec_file_location: str) -> dict:
    """Read a spec file from the filesystem.

    :param spec_file_location: The path to the job spec file.
    """

    job_spec = self.jobspec.create_job_spec_from_filesystem(spec_file_location)
    click.echo(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    click.echo(job_spec['spec_file_location'])
    return job_spec['spec_file_content']

  def provision(self, spec_file_content: dict):
    """Begin provisioning the local machine.

    :param spec_file_content: A loaded job spec file.
    """

    filesystem = FileSystem(spec_file_content['workspace_root_path'])

    sudo = SUDO(filesystem)
    sudo.prompt_for_sudo()

    inventory = InventoryFile(spec_file_content)
    inventory.write_inventory_file()

    ansible_job = AnsibleRunner(spec_file_content)
    ansible_job.start()

  @staticmethod
  def version():
    """Report the Mac Maker version."""

    click.echo(
        "Mac Maker Version: "
        f"{pkg_resources.get_distribution('mac_maker').version}",
    )
