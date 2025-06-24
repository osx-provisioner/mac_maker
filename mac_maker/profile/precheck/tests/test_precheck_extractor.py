"""Test the PrecheckGenerator."""

from pathlib import Path
from unittest import mock

from mac_maker import config
from mac_maker.ansible_controller.spec import Spec
from mac_maker.profile.precheck import TypePrecheckFileData
from mac_maker.profile.precheck.precheck_extractor import PrecheckExtractor


class TestPrecheckExtractor:
  """Test the PrecheckExtractor Class."""

  mocked_textfile_reader_result = [
      "mocked_notes",
      "mocked_env",
  ]

  def test_get_precheck_data__reads_correct_files(
      self,
      global_spec_mock: Spec,
      mocked_textfile_read: mock.Mock,
      precheck_extractor_instance: PrecheckExtractor,
  ) -> None:
    mocked_textfile_read.side_effect = self.mocked_textfile_reader_result

    precheck_extractor_instance.get_precheck_data(global_spec_mock)

    assert mocked_textfile_read.mock_calls == [
        mock.call(
            Path(global_spec_mock.workspace_root_path) /
            config.PRECHECK['notes']
        ),
        mock.call(
            Path(global_spec_mock.workspace_root_path) / config.PRECHECK['env']
        ),
    ]

  def test_get_precheck_data__returns_correct_data(
      self,
      global_spec_mock: Spec,
      mocked_textfile_read: mock.Mock,
      precheck_extractor_instance: PrecheckExtractor,
  ) -> None:
    mocked_textfile_read.side_effect = self.mocked_textfile_reader_result

    result = precheck_extractor_instance.get_precheck_data(global_spec_mock)

    assert result == TypePrecheckFileData(
        notes=self.mocked_textfile_reader_result[0],
        env=self.mocked_textfile_reader_result[1],
    )
