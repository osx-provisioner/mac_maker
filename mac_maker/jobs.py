"""Jobs for the Mac Maker."""

import sys
from pathlib import Path
from typing import Union, cast

import click
from . import config
from .ansible_controller.inventory import InventoryFile
from .ansible_controller.runner import AnsibleRunner
from .utilities.github import GithubRepository
from .utilities.password import SUDO
from .utilities.precheck import PrecheckConfig, TypePrecheckFileData
from .utilities.spec import JobSpec
from .utilities.state import TypeState
from .utilities.workspace import WorkSpace


class Jobs:
  """Jobs for the Mac Maker."""

  def __init__(self) -> None:
    self.jobspec = JobSpec()

  def get_precheck_content_from_github(
      self, repository_url: str, branch_name: Union[None, str]
  ) -> TypePrecheckFileData:
    """Read the precheck data from a GitHub repository.

    :param repository_url: The GitHub Repository URL.
    :param branch_name: The GitHub Repository branch name.
    :returns: The precheck file data.
    """

    repo = GithubRepository(repository_url)
    precheck_data = repo.download_zip_bundle_files(
        branch_name,
        {
            'notes': str(config.PRECHECK['notes']),
            'env': str(config.PRECHECK['env']),
        },
    )
    return cast(TypePrecheckFileData, precheck_data)

  def get_precheck_content_from_spec(
      self,
      spec_file_location: str,
  ) -> TypePrecheckFileData:
    """Read the precheck data using a spec file.

    :param spec_file_location: The path to the spec file.
    :returns: The precheck file data.
    """

    precheck_data = self.jobspec.extract_precheck_from_job_spec(
        spec_file_location
    )
    return precheck_data

  def precheck(self, precheck_data: TypePrecheckFileData) -> None:
    """Precheck the profile for validity and environment variable content.

    :param precheck_data: The loaded precheck_data.
    """

    validator = PrecheckConfig(precheck_data['env'])
    validator.is_valid_env_file()
    results = validator.validate_environment()
    if not results['is_valid']:
      for violation in results['violations']:
        click.echo(violation)
      sys.exit(1)
    click.echo(precheck_data['notes'])

  def create_state_from_github_spec(
      self, repository_url: str, branch_name: Union[None, str]
  ) -> TypeState:
    """Fetch a GitHub zip bundle, and build a state object.

    :param repository_url: The GitHub Repository URL.
    :param branch_name: The GitHub Repository branch name.
    :returns: The created state object.
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

  def create_state_from_local_spec_file(
      self, spec_file_location: Union[Path, str]
  ) -> TypeState:
    """Read a spec file from the filesystem and build a state object.

    :param spec_file_location: The path to the job spec file.
    :returns: The created state object.
    """

    job_spec = self.jobspec.create_job_spec_from_filesystem(spec_file_location)
    click.echo(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    click.echo(job_spec['spec_file_location'])
    return job_spec['spec_file_content']

  def provision(self, loaded_state: TypeState) -> None:
    """Begin provisioning the local machine.

    :param loaded_state: A loaded job spec as state.
    """
    sudo = SUDO()
    sudo.prompt_for_sudo()

    inventory = InventoryFile(loaded_state)
    inventory.write_inventory_file()

    ansible_job = AnsibleRunner(loaded_state)
    ansible_job.start()
