"""Provisioning spec derived from a Mac Maker profile."""

from pathlib import Path
from typing import TypedDict, Union

from mac_maker.utilities.state import TypeState


class TypeSpecFileData(TypedDict):
  """Typed representation of a loaded Job Spec file."""

  spec_file_content: TypeState
  spec_file_location: Union[Path, str]
