"""Provisioning pre-application checks for a Mac Maker profile."""

from typing import List, TypedDict


class TypePrecheckFileData(TypedDict):
  """Typed representation of a Precheck's complete contents."""

  notes: str
  env: str


class TypePrecheckEnvironmentValidationResult(TypedDict):
  """Typed representation of a precheck environment variable validation."""

  is_valid: bool
  violations: List[str]


class TypePrecheckVariableDefinition(TypedDict):
  """Typed representation of a precheck environment variable definition."""

  name: str
  description: str
