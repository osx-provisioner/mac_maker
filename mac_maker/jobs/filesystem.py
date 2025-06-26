"""A provisioning job for a Job Spec file on the local file system."""

from typing import Optional, cast

import click
from mac_maker import config
from mac_maker.jobs import bases
from mac_maker.utilities.precheck import TypePrecheckFileData
from mac_maker.utilities.spec import TypeSpecFileData
from mac_maker.utilities.state import TypeState


class FileSystemJob(bases.ProvisionerJobBase):
  """A provisioning job for a Job Spec file on the local file system.

  :param spec_file_location: The path to the Job Spec file.
  """

  spec_file_location: str
  job_spec_data: Optional[TypeSpecFileData]

  def __init__(self, spec_file_location: str):
    super().__init__()
    self.spec_file_location = spec_file_location
    self.job_spec_data = None

  def _extract_precheck_data(self) -> None:
    """Extract Precheck data from a loaded Job Spec file."""
    if not self.job_spec_data:
      self.job_spec_data = self.jobspec_extractor.get_job_spec_data(
          self.spec_file_location
      )

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the Precheck data defined in a Job Spec file.

    :returns: The Precheck file data.
    """

    self._extract_precheck_data()
    precheck_data = self.precheck_extractor.get_precheck_data(
        cast(TypeSpecFileData, self.job_spec_data)
    )

    return precheck_data

  def get_state(self) -> TypeState:
    """Read a Job Spec file and build a runtime state object.

    :returns: The created runtime state object.
    """

    self._extract_precheck_data()
    click.echo(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    job_spec_data = cast(TypeSpecFileData, self.job_spec_data)
    click.echo(job_spec_data['spec_file_location'])
    return job_spec_data['spec_file_content']
