"""Test the TextFile mixin classes."""

from unittest import TestCase, mock

from .. import text_file

TEXT_FILE_MODULE = text_file.__name__


@mock.patch('builtins.open')
class TextFileReaderTest(TestCase):
  """Test the TextFileReader mixin class."""

  def setUp(self) -> None:
    self.instance = text_file.TextFileReader()
    self.mock_context = mock.Mock()
    self.mock_path = "/mock/path"
    self.mock_text = "I am a mock string."

  def test_read_text_file_return_value(self, m_open: mock.Mock) -> None:
    m_open.return_value.__enter__.return_value.read.return_value = \
      self.mock_text
    result = self.instance.read_text_file(self.mock_path)
    self.assertEqual(result, self.mock_text)

  def test_read_text_file_call(self, m_open: mock.Mock) -> None:
    self.instance.read_text_file(self.mock_path)
    m_open.assert_called_once_with(
        self.mock_path, encoding=text_file.TextFileReader.encoding
    )
    m_open.return_value.__enter__.return_value.read.assert_called_once_with()


@mock.patch('builtins.open')
class TextFileWriterTest(TestCase):
  """Test the TextFileWriter class."""

  def setUp(self) -> None:
    self.instance = text_file.TextFileWriter()
    self.mock_context = mock.Mock()
    self.mock_path = "/mock/path"
    self.mock_text = "I am a mock string."

  def test_write_text_file_call(self, m_open: mock.Mock) -> None:
    self.instance.write_text_file(self.mock_text, self.mock_path)
    m_open.assert_called_once_with(
        self.mock_path, "w", encoding=text_file.TextFileReader.encoding
    )
    m_open.return_value.__enter__.return_value.write.assert_called_once_with(
        self.mock_text
    )
