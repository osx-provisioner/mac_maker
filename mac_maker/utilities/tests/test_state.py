"""Test the State class."""

import json
from io import StringIO
from logging import Logger
from pathlib import Path
from unittest import TestCase, mock

from .. import state

STATE_MODULE = state.__name__


class TestStateClass(TestCase):
  """Test the State class."""

  def setUp(self):
    self.state = state.State()
    self.mock_state_data = {
        "one": "two"
    }
    self.mock_state_file_name = Path("spec.json")

  def test_init_settings(self):
    self.assertIsInstance(
        self.state.log,
        Logger,
    )

  @mock.patch('builtins.open')
  def test_state_dehydrate(self, m_open):

    mock_file = StringIO()
    m_open.return_value.__enter__.return_value = mock_file
    result = self.state.state_dehydrate(
        self.mock_state_data,
        self.mock_state_file_name,
    )
    m_open.assert_called_once_with(self.mock_state_file_name, "w")

    self.assertDictEqual(
        self.mock_state_data,
        json.loads(mock_file.getvalue()),
    )

    self.assertDictEqual(result, self.mock_state_data)

  @mock.patch('builtins.open')
  def test_state_rehydrate(self, m_open):
    mock_file = StringIO(json.dumps(self.mock_state_data))
    m_open.return_value.__enter__.return_value = mock_file

    result = self.state.state_rehydrate(self.mock_state_file_name)

    m_open.assert_called_once_with(self.mock_state_file_name)

    self.assertDictEqual(result, self.mock_state_data)
