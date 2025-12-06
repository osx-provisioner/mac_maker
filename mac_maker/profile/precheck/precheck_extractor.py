"""Extractor for a profile's precheck data."""

from pathlib import Path

from mac_maker import config
from mac_maker.ansible_controller.spec import Spec
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.utilities.mixins.text_file import TextFileReader


class PrecheckExtractor(TextFileReader):
  """Extractor for a profile's precheck data."""

  def get_precheck_data(
      self,
      spec: Spec,
  ) -> TypePrecheckFileData:
    """Read a profile's precheck data and return it.

    :param spec: The provisioning spec instance.
    :returns: The complete precheck contents.
    """
    workspace_root = Path(spec.workspace_root_path)
    return TypePrecheckFileData(
        notes=self.read_text_file(workspace_root / config.PRECHECK['notes']),
        env=self.read_text_file(workspace_root / config.PRECHECK['env']),
    )
