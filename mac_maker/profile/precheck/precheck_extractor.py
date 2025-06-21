"""Extractor for a profile's precheck data."""

from pathlib import Path

from mac_maker import config
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.profile.spec_file import TypeSpecFileData
from mac_maker.utilities.mixins.text_file import TextFileReader


class PrecheckExtractor(TextFileReader):
  """Extractor for a profile's precheck data."""

  def get_precheck_data(
      self,
      spec_file_data: TypeSpecFileData,
  ) -> TypePrecheckFileData:
    """Read a profile's precheck data and return it.

    :param spec_file_data: A loaded spec file.
    :returns: The complete precheck contents.
    """
    workspace_root = Path(
        spec_file_data['spec_file_content']['workspace_root_path']
    )
    return TypePrecheckFileData(
        notes=self.read_text_file(workspace_root / config.PRECHECK['notes']),
        env=self.read_text_file(workspace_root / config.PRECHECK['env']),
    )
