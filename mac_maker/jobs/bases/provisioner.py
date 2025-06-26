"""ProvisionerJobBase class."""

import abc
import sys

import click
from mac_maker.ansible_controller.inventory import AnsibleInventoryFile
from mac_maker.ansible_controller.runner import AnsibleRunner
from mac_maker.ansible_controller.spec import Spec
from mac_maker.config import PRECHECK_SUCCESS_MESSAGE
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.profile.precheck.precheck_extractor import PrecheckExtractor
from mac_maker.profile.precheck.precheck_validator import PrecheckValidator
from mac_maker.profile.spec_file import SpecFile
from mac_maker.utilities.sudo import SUDO


class ProvisionerJobBase(abc.ABC):
  """Job base class, with Ansible provisioning."""

  def __init__(self) -> None:
    self.spec_file = SpecFile()
    self.precheck_extractor = PrecheckExtractor()

  @abc.abstractmethod
  def get_precheck_content(self) -> TypePrecheckFileData:
    """Extract the Profile's Precheck file contents."""
    raise NotImplementedError  # nocover

  @abc.abstractmethod
  def get_spec(self) -> Spec:
    """Assemble and return a provisioning spec instance."""
    raise NotImplementedError  # nocover

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

    click.echo(PRECHECK_SUCCESS_MESSAGE)

  def provision(self) -> None:
    """Begin provisioning with Ansible."""

    spec = self.get_spec()

    sudo = SUDO()
    sudo.prompt_for_sudo()

    inventory = AnsibleInventoryFile(spec)
    inventory.write()

    ansible_job = AnsibleRunner(spec)
    ansible_job.start()
