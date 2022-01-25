"""Job base classes for the Mac Maker."""

import abc
import sys

import click
from ..ansible_controller.inventory import InventoryFile
from ..ansible_controller.runner import AnsibleRunner
from ..utilities.password import SUDO
from ..utilities.spec import JobSpec
from ..utilities.state import TypeState
from ..utilities.validation.precheck import (
  PrecheckConfigValidator,
  TypePrecheckFileData,
)


class SimpleJobBase(abc.ABC):
  """Job base class for the Mac Maker, that doesn't require provisioning."""

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke a simple Job that doesn't require provisioning."""
    raise NotImplementedError  # nocover


class ProvisionerJobBase(abc.ABC):
  """Job base class for the Mac Maker."""

  def __init__(self) -> None:
    self.jobspec = JobSpec()

  @abc.abstractmethod
  def get_precheck_content(self) -> TypePrecheckFileData:
    """Extract the profile's precheck file contents."""
    raise NotImplementedError  # nocover

  @abc.abstractmethod
  def get_state(self) -> TypeState:
    """Assemble and return a state object."""
    raise NotImplementedError  # nocover

  def precheck(self) -> None:
    """Precheck the profile for validity and environment variable content."""

    precheck_data = self.get_precheck_content()

    validator = PrecheckConfigValidator(precheck_data['env'])
    validator.validate_config()
    results = validator.validate_environment()
    if not results['is_valid']:
      for violation in results['violations']:
        click.echo(violation)
      sys.exit(1)
    click.echo(precheck_data['notes'])

  def provision(self) -> None:
    """Begin provisioning the local machine."""

    loaded_state = self.get_state()

    sudo = SUDO()
    sudo.prompt_for_sudo()

    inventory = InventoryFile(loaded_state)
    inventory.write_inventory_file()

    ansible_job = AnsibleRunner(loaded_state)
    ansible_job.start()
