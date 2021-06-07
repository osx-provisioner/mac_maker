"""AnsibleRunner workflow class."""

import logging

import click
from .. import config
from .process import AnsibleProcess


class AnsibleRunner:
  """AnsibleRunner workflow class."""

  def __init__(self, state_object: dict, debug: bool = False):
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.debug = debug
    self.state = state_object

  def start(self) -> None:
    """Starts the Ansible provisioning workflow."""

    galaxy_roles_command = self._construct_galaxy_roles_command()
    galaxy_col_command = self._construct_galaxy_col_command()
    playbook_command = self._construct_ansible_playbook_command()

    self._do_ansible_galaxy_roles(galaxy_roles_command)
    self._do_ansible_galaxy_col(galaxy_col_command)
    self._do_ansible_playbook(playbook_command)

  def _construct_galaxy_roles_command(self) -> str:

    requirements_file = self.state['galaxy_requirements_file']
    role_path = self.state['roles_path'][0]
    self.log.debug(
        "AnsibleRunner: Reading Profile Requirements from: %s",
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
        "AnsibleRunner: Reading Profile Requirements from: %s",
        requirements_file,
    )
    command = (
        f"ansible-galaxy collection install -r {requirements_file}"
        f" -p {col_path}"
    )
    return command

  def _construct_ansible_playbook_command(self) -> str:

    self.log.debug("AnsibleRunner: Invoking Ansible")
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

  def _do_ansible_galaxy_roles(self, galaxy_command):
    controller = AnsibleProcess(
        config.ANSIBLE_LIBRARY_GALAXY_MODULE,
        config.ANSIBLE_LIBRARY_GALAXY_CLASS,
        self.state,
    )

    click.echo(config.ANSIBLE_ROLES_MESSAGE)
    controller.spawn(galaxy_command)
    self.log.debug(
        "AnsibleRunner: Profile Galaxy Roles have been installed to: %s",
        self.state['roles_path'][0],
    )

  def _do_ansible_galaxy_col(self, galaxy_command):
    controller = AnsibleProcess(
        config.ANSIBLE_LIBRARY_GALAXY_MODULE,
        config.ANSIBLE_LIBRARY_GALAXY_CLASS,
        self.state,
    )

    click.echo(config.ANSIBLE_COLLECTIONS_MESSAGE)
    controller.spawn(galaxy_command)
    self.log.debug(
        "AnsibleRunner: Profile Galaxy Collections have been installed to: %s",
        self.state['collections_path'][0],
    )

  def _do_ansible_playbook(self, ansible_command):
    controller = AnsibleProcess(
        config.ANSIBLE_LIBRARY_PLAYBOOK_MODULE,
        config.ANSIBLE_LIBRARY_PLAYBOOK_CLASS,
        self.state,
    )

    click.echo(config.ANSIBLE_INVOKE_MESSAGE)
    controller.spawn(ansible_command)
    self.log.debug("AnsibleRunner: Ansible Playbook has finished.",)
