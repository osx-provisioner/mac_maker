"""A provisioning job for a spec file on the local file system."""

from typing import Optional

import click
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.profile.spec_file import TypeSpecFileData
from mac_maker.utilities.state import TypeState
from .. import config
from .bases.provisioner import ProvisionerJobBase


class SpecFileJob(ProvisionerJobBase):
  """A provisioning job for a spec file on the local file system.

  :param spec_file_location: The path to the spec file.
  """

  spec_file_location: str
  spec_file_content: Optional[TypeSpecFileData]

  def __init__(self, spec_file_location: str):
    super().__init__()
    self.spec_file_location = spec_file_location
    self.spec_file_content = None

  def _extract_spec_file_data(self) -> TypeSpecFileData:
    if not self.spec_file_content:
      self.spec_file_content = self.spec_file_extractor.get_spec_file_data(
          self.spec_file_location
      )
    return self.spec_file_content

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the Precheck data defined in a spec file.

    :returns: The Precheck file data.
    """

    precheck_data = self.precheck_extractor.get_precheck_data(
        self._extract_spec_file_data()
    )

    return precheck_data

  def get_state(self) -> TypeState:
    """Read a spec file and build a runtime state object.

    :returns: The created runtime state object.
    """

    spec_file_data = self._extract_spec_file_data()
    click.echo(config.SPEC_FILE_LOADED_MESSAGE)
    click.echo(spec_file_data['spec_file_location'])
    return spec_file_data['spec_file_content']
