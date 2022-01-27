"""A provisioning job for a spec file and profile on the local file system."""

from typing import Optional, cast

import click
from .. import config
from ..utilities.precheck import TypePrecheckFileData
from ..utilities.spec import TypeSpecFileData
from ..utilities.state import TypeState
from . import bases


class FileSystemJob(bases.ProvisionerJobBase):
  """A provisioning job for a spec file and profile on the local file system.

  :param spec_file_location: The path to the spec file.
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
    """Read the precheck data using a spec file.

    :returns: The precheck file data.
    """

    self._extract_precheck_data()
    precheck_data = self.precheck_extractor.get_precheck_data(
        cast(TypeSpecFileData, self.job_spec_data)
    )

    return precheck_data

  def get_state(self) -> TypeState:
    """Read a spec file from the filesystem and build a state object.

    :returns: The created state object.
    """

    self._extract_precheck_data()
    click.echo(config.ANSIBLE_JOB_SPEC_READ_MESSAGE)
    job_spec_data = cast(TypeSpecFileData, self.job_spec_data)
    click.echo(job_spec_data['spec_file_location'])
    return job_spec_data['spec_file_content']
