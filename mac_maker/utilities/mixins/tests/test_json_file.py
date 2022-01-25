"""Test the JSONFile mixin classes."""

import json
from unittest import TestCase, mock

from .. import json_file

JSON_FILE_MODULE = json_file.__name__


@mock.patch(JSON_FILE_MODULE + '.json')
@mock.patch('builtins.open')
class JSONFileReaderTest(TestCase):
  """Test the JSONFileReader mixin class."""

  def setUp(self) -> None:
    self.instance = json_file.JSONFileReader()
    self.mock_object = {
        "mock": "object"
    }
    self.mock_json = json.dumps(self.mock_object)
    self.mock_context = mock.Mock()

  def test_load_json_file_return_value(
      self,
      m_open: mock.Mock,
      m_json: mock.Mock,
  ) -> None:
    mock_path = "/mock/path"
    self.mock_context.return_value = self.mock_json
    m_open.return_value.__enter__.return_value = self.mock_context
    m_json.load.return_value = self.mock_object

    result = self.instance.load_json_file(mock_path)
    self.assertEqual(result, self.mock_object)

  def test_load_json_file_call(
      self,
      m_open: mock.Mock,
      m_json: mock.Mock,
  ) -> None:
    mock_path = "/mock/path"
    m_open.return_value.__enter__.return_value = self.mock_context

    self.instance.load_json_file(mock_path)

    m_json.load.assert_called_once_with(self.mock_context)


@mock.patch(JSON_FILE_MODULE + '.json')
@mock.patch('builtins.open')
class JSONFileWriterTest(TestCase):
  """Test the JSONFileReader mixin class."""

  def setUp(self) -> None:
    self.instance = json_file.JSONFileWriter()
    self.mock_object = {
        "mock": "object"
    }
    self.mock_json = json.dumps(self.mock_object)
    self.mock_context = mock.Mock()

  def test_write_json_file_call(
      self,
      m_open: mock.Mock,
      m_json: mock.Mock,
  ) -> None:
    mock_path = "/mock/path"
    self.mock_context.return_value = self.mock_json
    m_open.return_value.__enter__.return_value = self.mock_context

    self.instance.write_json_file(self.mock_object, mock_path)

    m_json.dump.assert_called_once_with(self.mock_object, self.mock_context)
