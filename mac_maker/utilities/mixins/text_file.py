"""TextFile mixin classes."""

from pathlib import Path
from typing import Union


class TextFileReader:
  """TextFileReader mixin class."""

  encoding = "utf-8"

  def read_text_file(self, text_file_location: Union[Path, str]) -> str:
    """Load a text file from the file system and return it as a string.

    :param text_file_location: The path to the source file.
    :returns: The loaded string object.
    """
    with open(text_file_location, encoding=self.encoding) as file_handle:
      data = file_handle.read()
    return data


class TextFileWriter:
  """TextFileWriter mixin class."""

  encoding = "utf-8"

  def write_text_file(
      self, text_file_content: str, text_file_location: Union[Path, str]
  ) -> None:
    """Load a text file from the file system and return it as a string.

    :param text_file_content: The content to write to the file.
    :param text_file_location: The path to the source file.
    :returns: The loaded string object.
    """
    with open(text_file_location, "w", encoding=self.encoding) as file_handle:
      file_handle.write(text_file_content)
