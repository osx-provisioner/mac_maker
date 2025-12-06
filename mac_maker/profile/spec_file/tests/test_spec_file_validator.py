"""Test the SpecFileValidator class."""

import json
from logging import Logger
from pathlib import Path

import mac_maker
import pytest
from mac_maker.profile.spec_file import exceptions
from mac_maker.profile.spec_file.spec_file_validator import SpecFileValidator
from mac_maker.tests import fixtures


class TestSpecFileValidator:
  """Test the SpecFileValidator class."""

  spec_data_valid = json.loads(
      (Path(fixtures.__file__).parent /
       "mock_v1_spec_file.json").read_text(encoding="utf-8")
  )
  spec_data_invalid = json.loads(
      (Path(fixtures.__file__).parent /
       "mock_v1_invalid_spec_file.json").read_text(encoding="utf-8")
  )

  def test_initializer__attributes(self) -> None:
    instance = SpecFileValidator(self.spec_data_valid)

    assert instance.spec_file_json_content == self.spec_data_valid
    assert isinstance(instance.log, Logger)
    assert instance.schema_definition == (
        Path(mac_maker.__file__).parent / "schemas" / "spec_file_v1.json"
    )
    assert instance.schema == instance.load_json_file(
        instance.schema_definition
    )

  def test_validate__invalid_content__raises_exception(self) -> None:
    instance = SpecFileValidator(self.spec_data_invalid)

    with pytest.raises(exceptions.SpecFileValidationError) as exc:
      instance.validate()

    assert json.loads(exc.value.args[0]) == [
        "'collections_path' is a required property",
        "'roles_path' is a required property",
    ]

  def test_validate__valid_content__no_exception(self) -> None:
    instance = SpecFileValidator(self.spec_data_valid)

    instance.validate()
