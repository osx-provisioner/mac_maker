"""Test the State class."""

import json
import os
from io import StringIO
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

  def test_init_settings(self) -> None:
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

  @mock.patch('builtins.open')
  def test_state_dehydrate(self, m_open: mock.Mock) -> None:

    mock_file = StringIO()
    m_open.return_value.__enter__.return_value = mock_file
    self.state.state_dehydrate(
        cast(state.TypeState, self.mock_state_data),
        self.mock_state_file_name,
    )
    m_open.assert_called_once_with(
        self.mock_state_file_name, "w", encoding="utf-8"
    )

    self.assertDictEqual(
        self.mock_state_data,
        json.loads(mock_file.getvalue()),
    )

  @mock.patch('builtins.open')
  def test_state_rehydrate(self, m_open: mock.Mock) -> None:
    mock_file = StringIO(json.dumps(self.mock_state_data))
    m_open.return_value.__enter__.return_value = mock_file

    result = self.state.state_rehydrate(self.mock_state_file_name)

    m_open.assert_called_once_with(self.mock_state_file_name, encoding="utf-8")

    self.assertDictEqual(result, self.mock_state_data)
