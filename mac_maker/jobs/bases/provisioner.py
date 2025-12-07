"""ProvisionerJobBase class."""

import abc
import sys

import click
from mac_maker.ansible_controller.inventory import AnsibleInventoryFile
from mac_maker.ansible_controller.runner import AnsibleRunner
from mac_maker.ansible_controller.spec import Spec
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.profile.precheck.precheck_extractor import PrecheckExtractor
from mac_maker.profile.precheck.precheck_validator import PrecheckValidator
from mac_maker.profile.spec_file import SpecFile, SpecFileContentNotDefined
from mac_maker.utilities.sudo import SUDO


class ProvisionerJobBase(abc.ABC):
  """Job base class, with Ansible provisioning."""

  class Messages:
    precheck_success = "Ready to proceed!"
    spec_file_loaded = "--- Spec Loaded ---"

  def __init__(self) -> None:
    self.spec_file = SpecFile()
    self.precheck_extractor = PrecheckExtractor()

  @abc.abstractmethod
  def initialize_spec_file(self) -> None:
    """Initialize the spec file for this provisioning job."""

  def _initialize_spec_file(self) -> None:
    """Conditionally intialize the spec file for this provisioning job."""

    try:
      self.spec_file.content
    except SpecFileContentNotDefined:
      self.initialize_spec_file()

  def get_precheck_content(self) -> TypePrecheckFileData:
    """Extract the Profile's Precheck file contents.

    :returns: The Precheck file data.
    """

    self._initialize_spec_file()
    precheck_data = self.precheck_extractor.get_precheck_data(
        self.spec_file.content
    )
    return precheck_data

  def get_spec(self) -> Spec:
    """Assemble and return a provisioning spec instance.

    :returns: The provisioning spec instance.
    """

    self._initialize_spec_file()
    click.echo(self.Messages.spec_file_loaded)
    click.echo(self.spec_file.path)
    return self.spec_file.content

  def precheck(self, notes: bool = True) -> None:
    """Precheck the Profile for validity and environment variable content.

    :param notes: A boolean indicating whether to display the Precheck notes.
    """

    precheck_data = self.get_precheck_content()

    validator = PrecheckValidator(precheck_data['env'])
    validator.validate_config()
    results = validator.validate_environment()
    if not results['is_valid']:
      for violation in results['violations']:
        click.echo(violation)
      sys.exit(1)

    if notes:
      click.echo(precheck_data['notes'])

    click.echo(self.Messages.precheck_success)

  def provision(self) -> None:
    """Begin provisioning with Ansible."""

    spec = self.get_spec()

    sudo = SUDO()
    sudo.prompt_for_sudo()

    inventory = AnsibleInventoryFile(spec)
    inventory.write()

    ansible_job = AnsibleRunner(spec)
    ansible_job.start()
