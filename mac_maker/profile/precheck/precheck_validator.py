"""Profile precheck data validator."""

import os
from pathlib import Path
from typing import List

import mac_maker
import yaml
from jsonschema import ValidationError, validate
from mac_maker.profile.precheck import (
    TypePrecheckEnvironmentValidationResult,
    TypePrecheckVariableDefinition,
)
from mac_maker.profile.precheck.exceptions import PrecheckValidationError
from mac_maker.utilities.mixins.json_file import JSONFileReader


class PrecheckValidator(JSONFileReader):
  """Profile precheck data validator.

  :param env_config_file_data: Contents of a Precheck environment config file.
  :raises: :class:`exceptions.PrecheckConfigValidationError`
  """

  class Messages:
    syntax_error = "Invalid YAML syntax."
    error_template = (
        "ERROR: environment variable {name} is undefined.\n"
        "DESCRIPTION: {description}\n"
    )

  schema_definition = (
      Path(os.path.dirname(mac_maker.__file__)) / "schemas" / "env_v1.json"
  )

  def __init__(self, env_config_file_data: str) -> None:
    self.schema = self.load_json_file(self.schema_definition)

    try:
      self.parsed_yaml: List[TypePrecheckVariableDefinition] = yaml.safe_load(
          env_config_file_data
      )
    except yaml.YAMLError as exc:
      raise PrecheckValidationError(self.Messages.syntax_error) from exc

  def validate_config(self) -> None:
    """Validate an precheck environment config file.

    :raises: :class:`PrecheckConfigValidationException`
    """

    try:
      validate(self.parsed_yaml, self.schema)
    except ValidationError as exc:
      raise PrecheckValidationError(self.Messages.syntax_error) from exc

  def validate_environment(self) -> TypePrecheckEnvironmentValidationResult:
    """Validate the current environment against the parsed configuration file.

    :returns: The results of the environment validation as a hash.
    """

    violations = []
    for definition in self.parsed_yaml:
      environment_variable_name = definition['name']
      if environment_variable_name not in os.environ:
        violations.append(self._env_validation_error(definition))

    return {
        'is_valid': not violations,
        'violations': violations,
    }

  def _env_validation_error(
      self,
      variable_definition: TypePrecheckVariableDefinition,
  ) -> str:
    return self.Messages.error_template.format(**variable_definition)
