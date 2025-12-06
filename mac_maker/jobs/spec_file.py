"""A provisioning job for a spec file on the local file system."""

import click
from mac_maker import config
from mac_maker.ansible_controller.spec import Spec
from mac_maker.jobs.bases.provisioner import ProvisionerJobBase
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.profile.spec_file.exceptions import SpecFileContentNotDefined


class SpecFileJob(ProvisionerJobBase):
  """A provisioning job for a spec file on the local file system.

  :param spec_file_location: The path to the spec file.
  """

  spec_file_location: str

  def __init__(self, spec_file_location: str):
    super().__init__()
    self.spec_file.path = spec_file_location

  def _load_spec_file_content(self) -> None:
    try:
      self.spec_file.content
    except SpecFileContentNotDefined:
      self.spec_file.load()

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Read the Precheck data defined in a spec file.

    :returns: The Precheck file data.
    """

    self._load_spec_file_content()
    precheck_data = self.precheck_extractor.get_precheck_data(
        self.spec_file.content
    )

    return precheck_data

  def get_spec(self) -> Spec:
    """Assemble and return a provisioning spec instance.

    :returns: The created provisioning spec instance.
    """

    self._load_spec_file_content()
    click.echo(config.SPEC_FILE_LOADED_MESSAGE)
    click.echo(self.spec_file.path)
    return self.spec_file.content
