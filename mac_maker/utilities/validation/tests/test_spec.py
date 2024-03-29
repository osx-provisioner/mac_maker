"""Test the SpecFileValidator class."""

import json
from logging import Logger

from ....tests.fixtures import fixtures_spec
from .. import spec

SPEC_MODULE = spec.__name__


class TestSpecFileValidatorClass(fixtures_spec.SpecFileTestHarness):
  """Test the JobSpecExtractor class."""

  def test_init_settings(self) -> None:
    valid_spec_data = self.json_reader.load_json_file(
        self.fixtures_folder / "mock_v1_job_spec.json"
    )
    validator = spec.SpecFileValidator(valid_spec_data)
    self.assertIsInstance(
        validator.log,
        Logger,
    )
    self.assertIsInstance(
        validator.schema,
        dict,
    )
    self.assertEqual(
        validator.spec_file_content,
        valid_spec_data,
    )


class TestSpecValidity(fixtures_spec.SpecFileTestHarness):
  """Test the JobSpecExtractor class validation methods."""

  def test_v1_spec_valid(self) -> None:
    valid_spec_data = self.json_reader.load_json_file(
        self.fixtures_folder / "mock_v1_job_spec.json"
    )
    validator = spec.SpecFileValidator(valid_spec_data)
    validator.validate_spec_file()

  def test_v1_spec_invalid(self) -> None:
    invalid_spec_data = self.json_reader.load_json_file(
        self.fixtures_folder / "mock_v1_invalid_job_spec.json"
    )
    validator = spec.SpecFileValidator(invalid_spec_data)

    with self.assertRaises(spec.SpecFileValidationException) as exc:
      validator.validate_spec_file()

    self.assertListEqual(
        json.loads(exc.exception.args[0]), [
            "'collections_path' is a required property",
            "'roles_path' is a required property",
        ]
    )
