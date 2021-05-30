"""Profile precheck validator."""

import os

import yaml


class PrecheckConfigException(BaseException):
  """Raised when reading an invalid Precheck YAML configuration file."""


class PrecheckConfig:
  """Profile precheck validator."""

  syntax_error = "Invalid YAML syntax."

  def __init__(self, yaml_document):
    try:
      self.parsed_yaml = yaml.safe_load(yaml_document)
    except yaml.YAMLError as exc:
      raise PrecheckConfigException from exc

  def is_valid_env_file(self):
    """Validate an environment variable requirements file."""

    self._validate_is_list()
    self._validate_contains_env_dictionaries()

  def _validate_is_list(self):
    if not isinstance(self.parsed_yaml, list):
      raise PrecheckConfigException(self.syntax_error)

  def _validate_contains_env_dictionaries(self):
    for instance in self.parsed_yaml:
      if isinstance(instance, dict):
        if 'name' in instance and 'description' in instance:
          continue
      raise PrecheckConfigException(self.syntax_error)

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
