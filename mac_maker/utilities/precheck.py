"""Extractor for Precheck data specified in a Job Spec file."""

from pathlib import Path
from typing import TypedDict

from .. import config
from .mixins.text_file import TextFileReader
from .spec import TypeSpecFileData


class TypePrecheckFileData(TypedDict):
  """Typed representation of a Precheck's complete contents."""

  notes: str
  env: str


class PrecheckExtractor(TextFileReader):
  """Extractor for Precheck data specified in a Job Spec file."""

  def get_precheck_data(
      self,
      spec_file_data: TypeSpecFileData,
  ) -> TypePrecheckFileData:
    """Locate the Precheck data from a Job Spec file, and return it.

    :param spec_file_data: A loaded Job Spec file, and it's location.
    :returns: The complete Precheck contents.
    """
    workspace_root = Path(
        spec_file_data['spec_file_content']['workspace_root_path']
    )
    return TypePrecheckFileData(
        notes=self.read_text_file(workspace_root / config.PRECHECK['notes']),
        env=self.read_text_file(workspace_root / config.PRECHECK['env']),
    )
