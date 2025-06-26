"""Profile Precheck validator."""

import os
from pathlib import Path
from typing import List, TypedDict

import yaml
from jsonschema import ValidationError, validate
from mac_maker.utilities.mixins.json_file import JSONFileReader


class TypePrecheckEnvironmentValidationResult(TypedDict):
  """Typed representation of an Precheck environment validation result."""

  is_valid: bool
  violations: List[str]


class TypePrecheckVariableDefinition(TypedDict):
  """Typed representation of a Precheck environment variable definition."""

  name: str
  description: str


class PrecheckConfigValidationException(Exception):
  """Raised when reading an invalid Precheck environment configuration file."""


class PrecheckConfigValidator(JSONFileReader):
  """Profile Precheck validator.

  :param precheck_env_file: The path to a Precheck environment config file.
  :raises: :class:`PrecheckConfigValidationException`
  """

  syntax_error = "Invalid YAML syntax."
  schema_definition = (
      Path(os.path.dirname(__file__)).parent.parent / "schemas" / "env_v1.json"
  )

  def __init__(self, precheck_env_file: str) -> None:
    self.schema = self.load_json_file(self.schema_definition)

    try:
      self.parsed_yaml: List[TypePrecheckVariableDefinition] = yaml.safe_load(
          precheck_env_file
      )
    except yaml.YAMLError as exc:
      raise PrecheckConfigValidationException(self.syntax_error) from exc

  def validate_config(self) -> None:
    """Validate an Precheck environment config file.

    :raises: :class:`PrecheckConfigValidationException`
    """

    try:
      validate(self.parsed_yaml, self.schema)
    except ValidationError as exc:
      raise PrecheckConfigValidationException(self.syntax_error) from exc

  def validate_environment(self) -> TypePrecheckEnvironmentValidationResult:
    """Validate the environment against the parsed configuration file.

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
      self, variable_definition: TypePrecheckVariableDefinition
  ) -> str:
    return (
        "ERROR: "
        f"environment variable {variable_definition['name']} is undefined.\n"
        f"DESCRIPTION: {variable_definition['description']}\n"
    )
