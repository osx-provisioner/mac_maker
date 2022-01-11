"""Profile precheck validator."""

import json
import os
from pathlib import Path
from typing import Any, List, TypedDict

import yaml
from jsonschema import ValidationError, validate


class TypeEnvironmentValidationResult(TypedDict):
  """Typed representation of an environment validation result."""

  is_valid: bool
  violations: List[str]


class TypePrecheckVariableDefinition(TypedDict):
  """Typed representation of a precheck environment variable definition."""

  name: str
  description: str


class TypePrecheckFileData(TypedDict):
  """Typed representation of a precheck's file contents."""

  notes: str
  env: str


class PrecheckConfigException(BaseException):
  """Raised when reading an invalid Precheck YAML configuration file."""


class PrecheckConfig:
  """Profile precheck validator.

  :param yaml_document: The path to the YAML config file to read.
  """

  syntax_error = "Invalid YAML syntax."
  schema_definition = (
      Path(os.path.dirname(__file__)).parent / "schemas" / "env_v1.json"
  )

  def __init__(self, yaml_document: str) -> None:
    self.schema = self._load_schema()

    try:
      self.parsed_yaml: List[TypePrecheckVariableDefinition] = yaml.safe_load(
          yaml_document
      )
    except yaml.YAMLError as exc:
      raise PrecheckConfigException(self.syntax_error) from exc

  def _load_schema(self) -> Any:
    with open(self.schema_definition, encoding="utf-8") as fhandle:
      schema = json.load(fhandle)
    return schema

  def is_valid_env_file(self) -> None:
    """Validate an environment variable requirements file.

    :raises: :class:`PrecheckConfigException`
    """

    try:
      validate(self.parsed_yaml, self.schema)
    except ValidationError as exc:
      raise PrecheckConfigException(self.syntax_error) from exc

  def validate_environment(self) -> TypeEnvironmentValidationResult:
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
