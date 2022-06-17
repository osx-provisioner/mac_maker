"""Mac Maker configuration settings."""

from pathlib import Path

ENV_ANSIBLE_BECOME_PASSWORD = "ANSIBLE_BECOME_PASSWORD"  # nosec
ENV_ANSIBLE_ROLES_PATH = "ANSIBLE_ROLES_PATH"
ENV_ANSIBLE_COLLECTIONS_PATH = "ANSIBLE_COLLECTIONS_PATH"

ANSIBLE_LIBRARY_LOCALE_MODULE = "ansible.utils.display"
ANSIBLE_LIBRARY_GALAXY_MODULE = "ansible.cli.galaxy"
ANSIBLE_LIBRARY_GALAXY_CLASS = "GalaxyCLI"
ANSIBLE_LIBRARY_PLAYBOOK_MODULE = "ansible.cli.playbook"
ANSIBLE_LIBRARY_PLAYBOOK_CLASS = "PlaybookCLI"

ANSIBLE_INVOKE_MESSAGE = "--- Invoking Ansible Runner ---"
ANSIBLE_INVENTORY_CONTENT = (
    '[all]\n'
    'localhost\t'
    'ansible_connection=local\t'
)
ANSIBLE_JOB_SPEC_MESSAGE = "--- Job Spec Created ---"
ANSIBLE_JOB_SPEC_READ_MESSAGE = "--- Job Spec Loaded ---"
ANSIBLE_RETRIEVE_MESSAGE = "--- Retrieving Remote Profile ---"
ANSIBLE_ROLES_MESSAGE = "--- Installing Profile Roles ---"
ANSIBLE_COLLECTIONS_MESSAGE = "--- Installing Profile Collections ---"

GITHUB_HTTP_REGEX = r'http[s]?://github.com/(?P<org>.+)/(?P<repo>[^.]+)(\.git)?'
GITHUB_SSH_REGEX = r'git@github.com:(?P<org>.+)/(?P<repo>[^.]+)(\.git)?'
GITHUB_DEFAULT_BRANCH = 'master'

LOGGER_NAME = 'mac_maker'
LOGGER_FORMAT = '[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s'

PROFILE_FOLDER_PATH = "profile"
PROFILE_NOTES_FILE = "__precheck__/notes.txt"
PROFILE_ENVIRONMENT_FILE = "__precheck__/env.yml"
PROFILE_INSTALLER_FILE = "install.yml"
PROFILE_GALAXY_REQUIREMENTS_FILE = "requirements.yml"
PROFILE_INVENTORY_FILE = "inventory"

PRECHECK = {
    "notes": Path(PROFILE_FOLDER_PATH) / Path(PROFILE_NOTES_FILE),
    "env": Path(PROFILE_FOLDER_PATH) / Path(PROFILE_ENVIRONMENT_FILE)
}

STATE_FILE_NAME = "spec.json"

SUDO_PROMPT = "Please enter the SUDO password for your MAC: "
SUDO_CHECK_COMMAND = "sudo -kS /bin/echo"

WORKSPACE = 'installer.workspace'
