"""Profile precheck validator."""

import json
import os
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate


class PrecheckConfigException(BaseException):
  """Raised when reading an invalid Precheck YAML configuration file."""


class PrecheckConfig:
  """Profile precheck validator."""

  syntax_error = "Invalid YAML syntax."
  schema_definition = (
      Path(os.path.dirname(__file__)).parent / "schemas" / "env_v1.json"
  )

  def __init__(self, yaml_document):
    self.schema = self._load_schema()

    try:
      self.parsed_yaml = yaml.safe_load(yaml_document)
    except yaml.YAMLError as exc:
      raise PrecheckConfigException(self.syntax_error) from exc

  def _load_schema(self) -> dict:
    with open(self.schema_definition) as fhandle:
      schema = json.load(fhandle)
    return schema

  def is_valid_env_file(self):
    """Validate an environment variable requirements file."""

    try:
      validate(self.parsed_yaml, self.schema)
    except ValidationError as exc:
      raise PrecheckConfigException(self.syntax_error) from exc

  def validate_environment(self):
    """Validate the environment against the parsed configuration file."""

    violations = []
    for definition in self.parsed_yaml:
      environment_variable_name = definition['name']
      if environment_variable_name not in os.environ:
        violations.append(self._env_validation_error(definition))

    is_valid = violations == []
    return {
        'is_valid': is_valid,
        'violations': violations,
    }

  def _env_validation_error(self, variable_definition):
    return (
        "ERROR: "
        f"environment variable {variable_definition['name']} is undefined.\n"
        f"DESCRIPTION: {variable_definition['description']}\n"
    )
