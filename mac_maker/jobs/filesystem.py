"""A provisioning job for a spec file and profile on the local file system."""

import click
from .. import config
from ..utilities.precheck import TypePrecheckFileData
from ..utilities.state import TypeState
from . import bases


class FileSystemJob(bases.ProvisionerJobBase):
  """A provisioning job for a spec file and profile on the local file system.

  :param spec_file_location: The path to the spec file.
  """

  spec_file_location: str

  def __init__(self, spec_file_location: str):
    super().__init__()
    self.spec_file_location = spec_file_location

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the precheck data using a spec file.

    :returns: The precheck file data.
    """

    precheck_data = self.jobspec.extract_precheck_from_job_spec(
        self.spec_file_location
    )
    return precheck_data

  def get_state(self) -> TypeState:
    """Read a spec file from the filesystem and build a state object.

    :returns: The created state object.
    """

    job_spec = self.jobspec.create_job_spec_from_filesystem(
        self.spec_file_location
    )
    click.echo(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    click.echo(job_spec['spec_file_location'])
    return job_spec['spec_file_content']
