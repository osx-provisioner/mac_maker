"""A provisioning job for a spec file on the local file system."""

from mac_maker.jobs.bases.provisioner import ProvisionerJobBase


class SpecFileJob(ProvisionerJobBase):
  """A provisioning job for a spec file on the local file system.

  :param spec_file_location: The path to the spec file.
  """

  spec_file_location: str

  def __init__(self, spec_file_location: str):
    super().__init__()
    self.spec_file.path = spec_file_location

  def initialize_spec_file(self) -> None:
    """Initialize the spec file for this provisioning job."""

    self.spec_file.load()
