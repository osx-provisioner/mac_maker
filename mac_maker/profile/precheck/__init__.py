"""Provisioning pre-application checks for a Mac Maker profile."""

from typing import TypedDict


class TypePrecheckFileData(TypedDict):
  """Typed representation of a Precheck's complete contents."""

  notes: str
  env: str
