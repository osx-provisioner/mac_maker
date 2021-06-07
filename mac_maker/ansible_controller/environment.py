"""Ansible runtime environment class."""

import logging
import os
from typing import Dict

from .. import config


class Environment:

  def __init__(self, state: dict):
    self.log = logging.getLogger(config.LOGGER_NAME)
    self.env: Dict[str, str] = {}
    self.state = state

  def setup(self):
    self.log.debug(
        "Environment: configuring Ansible runtime environment variables..."
    )

    self.combine_env_with_state(config.ENV_ANSIBLE_ROLES_PATH, 'roles_path')
    self.combine_env_with_state(
        config.ENV_ANSIBLE_COLLECTIONS_PATH, 'collections_path'
    )
    self._save()
    self.log.debug("Environment: Ansible runtime environment is ready.")

  def combine_env_with_state(self, variable_name: str, state_name: str):
    existing_env_value = self._env_to_list(variable_name)
    existing_state_value = self._state_to_list(state_name)
    new_env_value = existing_state_value + existing_env_value
    self.env[variable_name] = self._list_to_env(new_env_value)

  def _env_to_list(self, variable_name: str) -> list:
    value = os.getenv(variable_name, None)
    if value is None:
      return []
    return value.split(":")

  def _state_to_list(self, state_name: str) -> list:
    return self.state[state_name]

  def _list_to_env(self, list_content: list) -> str:
    return ":".join(list_content)

  def _save(self):
    for key, value in self.env.items():
      os.environ[key] = value
