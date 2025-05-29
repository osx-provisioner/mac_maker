"""AnsibleRunner workflow class."""

import logging

import click
from .. import config
from ..utilities.state import TypeState
from . import process


class AnsibleRunner:
  """AnsibleRunner workflow class.

  :param state: The loaded runtime state object.
  :param debug: Enable or disable logs.
  """

  def __init__(self, state: TypeState, debug: bool = False):
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.debug = debug
    self.state = state
    self.process = process.AnsibleProcess(state)

  def start(self) -> None:
    """Start the Ansible provisioning workflow."""

    galaxy_roles_command = self._construct_galaxy_roles_command()
    galaxy_col_command = self._construct_galaxy_col_command()
    playbook_command = self._construct_ansible_playbook_command()

    try:
      self._do_install_galaxy_roles(galaxy_roles_command)
      self._do_install_galaxy_col(galaxy_col_command)
      self._do_ansible_playbook(playbook_command)
    except ChildProcessError:
      return

  def _construct_galaxy_roles_command(self) -> str:

    requirements_file = self.state['galaxy_requirements_file']
    role_path = self.state['roles_path'][0]
    self.log.debug(
        "AnsibleRunner: Reading Profile role requirements from: %s",
        requirements_file,
    )
    command = (
        f"ansible-galaxy role install -r {requirements_file}"
        f" -p {role_path}"
    )
    return command

  def _construct_galaxy_col_command(self) -> str:

    requirements_file = self.state['galaxy_requirements_file']
    col_path = self.state['collections_path'][0]
    self.log.debug(
        "AnsibleRunner: Reading Profile collection requirements from: %s",
        requirements_file,
    )
    command = (
        f"ansible-galaxy collection install -r {requirements_file}"
        f" -p {col_path}"
    )
    return command

  def _construct_ansible_playbook_command(self) -> str:

    command = (
        f"ansible-playbook {self.state['playbook']}"
        f" -i {self.state['inventory']}"
        " -e "
        "\"ansible_become_password="
        "'{{ lookup('env', 'ANSIBLE_BECOME_PASSWORD') }}'\""
    )
    if self.debug:
      command += " -vvvv"
    return command

  def _do_install_galaxy_roles(self, galaxy_command: str) -> None:
    click.echo(config.ANSIBLE_ROLES_MESSAGE)
    self.process.spawn(galaxy_command)
    self.log.debug(
        "AnsibleRunner: Profile Ansible Galaxy roles have been "
        "installed to: %s",
        self.state['roles_path'][0],
    )

  def _do_install_galaxy_col(self, galaxy_command: str) -> None:
    click.echo(config.ANSIBLE_COLLECTIONS_MESSAGE)
    self.process.spawn(galaxy_command)
    self.log.debug(
        "AnsibleRunner: Profile Ansible Galaxy collections have been "
        "installed to: %s",
        self.state['collections_path'][0],
    )

  def _do_ansible_playbook(self, ansible_command: str) -> None:
    click.echo(config.ANSIBLE_INVOKE_MESSAGE)
    self.log.debug("AnsibleRunner: Invoking Ansible ...")
    self.process.spawn(ansible_command)
    self.log.debug("AnsibleRunner: Ansible Playbook has finished!",)
