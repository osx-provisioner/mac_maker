"""JSONFile mixin classes."""

import json
from pathlib import Path
from typing import Any, Union


class JSONFileReader:
  """JSONFileReader mixin class."""

  encoding = "utf-8"

  def load_json_file(self, json_file_location: Union[Path, str]) -> Any:
    """Load a JSON file from the filesystem and return it as a Python object.

    :param json_file_location: The path to the source file.
    :returns: The loaded JSON object.
    """

    with open(json_file_location, encoding=self.encoding) as fhandle:
      json_file_content = json.load(fhandle)
    return json_file_content


class JSONFileWriter:
  """JSONFileWriter mixin class."""

  encoding = "utf-8"

  def write_json_file(
      self, python_object: Any, json_file_location: Union[Path, str]
  ) -> None:
    """Write a Python object to the filesystem as JSON.

    :param python_object: The Python object to write to file as JSON.
    :param json_file_location: The path to the destination file.
    """
    with open(json_file_location, "w", encoding=self.encoding) as file_handle:
      json.dump(python_object, file_handle)
