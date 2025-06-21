"""A provisioning job for a Job Spec file on the local file system."""

from typing import Optional

import click
from mac_maker import config
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.profile.spec_file import TypeSpecFileData
from mac_maker.utilities.state import TypeState


class SpecFileJob(ProvisionerJobBase):
  """A provisioning job for a Job Spec file on the local file system.

  :param spec_file_location: The path to the Job Spec file.
  """

  spec_file_location: str
  job_spec_data: Optional[TypeSpecFileData]

  def __init__(self, spec_file_location: str):
    super().__init__()
    self.spec_file_location = spec_file_location
    self.job_spec_data = None

  def _extract_job_spec_data(self) -> TypeSpecFileData:
    if not self.job_spec_data:
      self.job_spec_data = self.jobspec_extractor.get_job_spec_data(
          self.spec_file_location
      )
    return self.job_spec_data

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the Precheck data defined in a Job Spec file.

    :returns: The Precheck file data.
    """

    precheck_data = self.precheck_extractor.get_precheck_data(
        self._extract_job_spec_data()
    )

    return precheck_data

  def get_state(self) -> TypeState:
    """Read a Job Spec file and build a runtime state object.

    :returns: The created runtime state object.
    """

    job_spec_data = self._extract_job_spec_data()
    click.echo(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    click.echo(job_spec_data['spec_file_location'])
    return job_spec_data['spec_file_content']
