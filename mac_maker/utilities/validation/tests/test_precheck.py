"""Test precheck YAML configuration validator."""

from pathlib import Path
from typing import Any
from unittest import TestCase, mock

from mac_maker.tests import fixtures
from mac_maker.utilities.validation import precheck
from mac_maker.utilities.validation.precheck import (
    PrecheckConfigValidationException,
    PrecheckConfigValidator,
)

PRECHECK_MODULE = precheck.__name__


class TestValidator(TestCase):
  """Test the precheck YAML configuration validator."""

  def test_invalid_env_file(self) -> None:
    yaml_data = "not a list"
    validator = PrecheckConfigValidator(yaml_data)

    with self.assertRaises(PrecheckConfigValidationException) as exc:
      validator.validate_config()

    self.assertEqual(str(exc.exception), PrecheckConfigValidator.syntax_error)

  def test_correct(self) -> None:
    yaml_data = '[{"name" : "name", "description": "description"}]'
    validator = PrecheckConfigValidator(yaml_data)
    validator.validate_config()

    self.assertListEqual(
        validator.parsed_yaml, [{
            "name": "name",
            "description": "description"
        }]
    )

  def test_invalid_yaml(self) -> None:
    with self.assertRaises(PrecheckConfigValidationException):
      PrecheckConfigValidator('- dsfsdfs }: - dsfdsf')


class TestValidateEnv(TestCase):
  """Test the precheck environment validation method."""

  mock_yaml_data: Any

  @classmethod
  def setUpClass(cls) -> None:
    yaml_env_fixture = Path(fixtures.__file__).parent / "mock_env.yml"
    with open(yaml_env_fixture, encoding="utf-8") as fhandle:
      cls.mock_yaml_data = fhandle.read()

  def setUp(self) -> None:
    self.validator = PrecheckConfigValidator(self.mock_yaml_data)

  @mock.patch(PRECHECK_MODULE + ".os.environ", {})
  def test_validate_empty_environment(self) -> None:

    results = self.validator.validate_environment()

    var0 = self.validator.parsed_yaml[0]
    var1 = self.validator.parsed_yaml[1]

    self.assertFalse(results['is_valid'])
    self.assertListEqual(
        results['violations'], [
            (
                "ERROR: "
                f"environment variable {var0['name']} is undefined.\n"
                f"DESCRIPTION: {var0['description']}\n"
            ),
            (
                "ERROR: "
                f"environment variable {var1['name']} is undefined.\n"
                f"DESCRIPTION: {var1['description']}\n"
            ),
        ]
    )

  @mock.patch(PRECHECK_MODULE + ".os.environ", {"USER": "niall"})
  def test_validate_user_defined(self) -> None:
    results = self.validator.validate_environment()

    self.assertFalse(results['is_valid'])

    var1 = self.validator.parsed_yaml[1]
    self.assertListEqual(
        results['violations'], [
            (
                "ERROR: "
                f"environment variable {var1['name']} is undefined.\n"
                f"DESCRIPTION: {var1['description']}\n"
            ),
        ]
    )

  @mock.patch(
      PRECHECK_MODULE + ".os.environ", {
          "USER": "niall",
          "JUMPCLOUD_CONNECT_KEY": "11"
      }
  )
  def test_validate_all_defined(self) -> None:
    results = self.validator.validate_environment()

    self.assertTrue(results['is_valid'])
    self.assertListEqual(results['violations'], [])
