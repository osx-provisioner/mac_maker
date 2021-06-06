"""Mac Maker configuration settings"""

from pathlib import Path

ENV_ANSIBLE_BECOME_PASSWORD = "ANSIBLE_BECOME_PASSWORD"
ENV_ANSIBLE_ROLES_PATH = "ANSIBLE_ROLES_PATH"

ANSIBLE_INVOKE_MESSAGE = "--- Invoking Ansible Runner ---"
ANSIBLE_INVENTORY_CONTENT = (
    '[all]\n'
    'localhost\t'
    'ansible_connection=local\t'
    'ansible_python_interpreter=/usr/bin/python\n'
)
ANSIBLE_JOB_SPEC_MESSAGE = "--- Job Spec Created ---"
ANSIBLE_JOB_SPEC_READ_MESSAGE = "--- Job Spec Loaded ---"
ANSIBLE_RETRIEVE_MESSAGE = "--- Retrieving Remote Profile ---"
ANSIBLE_REQUIREMENTS_MESSAGE = "--- Installing Profile Requirements ---"

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
