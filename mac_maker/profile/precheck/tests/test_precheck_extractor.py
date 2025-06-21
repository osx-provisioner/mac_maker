"""Test the PrecheckGenerator."""

from pathlib import Path
from typing import cast
from unittest import TestCase, mock

from mac_maker import config
from mac_maker.profile.precheck import TypePrecheckFileData, precheck_extractor
from mac_maker.profile.spec_file import TypeSpecFileData
from mac_maker.utilities import state

PRECHECK_MODULE = precheck_extractor.__name__


@mock.patch(PRECHECK_MODULE + '.TextFileReader.read_text_file')
class TestSpecExtractPreCheckFromJobSpec(TestCase):
  """Test the JobSpecExtractor Class."""

  def setUp(self) -> None:
    self.spec = precheck_extractor.PrecheckExtractor()
    self.mock_spec_root = "/root/dir1"
    self.mock_spec_file_content = {
        "workspace_root_path": self.mock_spec_root
    }
    self.mock_spec_file_data = TypeSpecFileData(
        spec_file_location="/root/dir1",
        spec_file_content=cast(state.TypeState, self.mock_spec_file_content)
    )

    self.mock_notes = "notes content"
    self.mock_env = "env content"

  def test_get_precheck_data_result(self, m_read: mock.Mock) -> None:
    m_read.side_effect = [self.mock_notes, self.mock_env]

    result = self.spec.get_precheck_data(self.mock_spec_file_data)

    self.assertEqual(
        result, TypePrecheckFileData(notes=self.mock_notes, env=self.mock_env)
    )

  def test_get_precheck_data_calls(self, m_read: mock.Mock) -> None:
    m_read.side_effect = [self.mock_notes, self.mock_env]

    self.spec.get_precheck_data(self.mock_spec_file_data)

    expected1 = Path(self.mock_spec_root / config.PRECHECK['env'])
    expected2 = Path(self.mock_spec_root / config.PRECHECK['notes'])

    m_read.assert_any_call(expected1)
    m_read.assert_any_call(expected2)
    self.assertEqual(m_read.call_count, 2)
