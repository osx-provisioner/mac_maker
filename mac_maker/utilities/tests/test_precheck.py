"""Test precheck YAML configuration validator."""

from pathlib import Path
from unittest import TestCase, mock

from .. import precheck
from ..precheck import PrecheckConfig, PrecheckConfigException

PRECHECK_MODULE = precheck.__name__


class TestValidator(TestCase):
  """Test the precheck YAML configuration validator."""

  def test_invalid_env_file(self):
    yaml_data = "not a list"
    validator = PrecheckConfig(yaml_data)

    with self.assertRaises(PrecheckConfigException) as exc:
      validator.is_valid_env_file()

    self.assertEqual(str(exc.exception), PrecheckConfig.syntax_error)

  def test_correct(self):
    yaml_data = '[{"name" : "name", "description": "description"}]'
    validator = PrecheckConfig(yaml_data)
    validator.is_valid_env_file()

    self.assertListEqual(
        validator.parsed_yaml, [{
            "name": "name",
            "description": "description"
        }]
    )

  def test_invalid_yaml(self):
    with self.assertRaises(PrecheckConfigException):
      PrecheckConfig('- dsfsdfs }: - dsfdsf')


class TestValidateEnv(TestCase):
  """Test the precheck environment validation method."""

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    yaml_env_fixture = Path(__file__).parent / "fixtures" / "mock_env.yml"
    with open(yaml_env_fixture, encoding="utf-8") as fhandle:
      cls.mock_yaml_data = fhandle.read()

  def setUp(self):
    self.validator = PrecheckConfig(self.mock_yaml_data)

  @mock.patch(PRECHECK_MODULE + ".os.environ", {})
  def test_validate_empty_environment(self):

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
  def test_validate_user_defined(self):
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
  def test_validate_all_defined(self):
    results = self.validator.validate_environment()

    self.assertTrue(results['is_valid'])
    self.assertListEqual(results['violations'], [])
