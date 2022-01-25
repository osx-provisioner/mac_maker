"""Test the State class."""

import json
import os
from logging import Logger
from pathlib import Path
from typing import cast
from unittest import TestCase, mock

from jsonschema import validate
from .. import filesystem, state

STATE_MODULE = state.__name__


class TestStateClass(TestCase):
  """Test the State class."""

  def setUp(self) -> None:
    self.state = state.State()
    self.mock_state_data = {
        "one": "two"
    }
    self.mock_state_file_name = Path("spec.json")

    self.schema_definition = (
        Path(os.path.dirname(__file__)).parent.parent / "schemas" /
        "job_v1.json"
    )

  def test_init(self) -> None:
    self.assertIsInstance(
        self.state.log,
        Logger,
    )

  def test_state_generation_conforms_to_spec(self) -> None:
    with open(self.schema_definition, encoding="utf-8") as fhandle:
      schema = json.load(fhandle)

    mock_fs = filesystem.FileSystem("/root/mockdir")
    generated_state = self.state.state_generate(mock_fs)
    validate(generated_state, schema)

  @mock.patch(STATE_MODULE + ".JSONFileWriter.write_json_file")
  def test_state_dehydrate(self, m_write: mock.Mock) -> None:
    self.state.state_dehydrate(
        cast(state.TypeState, self.mock_state_data),
        self.mock_state_file_name,
    )
    m_write.assert_called_once_with(
        self.mock_state_data,
        self.mock_state_file_name,
    )

  @mock.patch(STATE_MODULE + ".JSONFileReader.load_json_file")
  def test_state_rehydrate(self, m_read: mock.Mock) -> None:
    m_read.return_value = self.mock_state_data
    result = self.state.state_rehydrate(self.mock_state_file_name)
    m_read.assert_called_once_with(self.mock_state_file_name)
    self.assertDictEqual(result, self.mock_state_data)
