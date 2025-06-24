"""Test the PrecheckValidator class."""
import os
from pathlib import Path
from unittest import mock

import mac_maker
import pytest
import yaml
from mac_maker.profile.precheck.exceptions import PrecheckValidationError
from mac_maker.profile.precheck.precheck_validator import PrecheckValidator
from mac_maker.tests import fixtures


class TestPrecheckValidator:
  """Test the PrecheckValidator class."""

  env_config_valid = (Path(fixtures.__file__).parent /
                      "mock_env.yml").read_text(encoding="utf-8")
  env_config_invalid = "invalid configuration"
  yaml_data_valid = '[{"name" : "name", "description": "description"}]'
  yaml_data_invalid = '- invalid }: - yaml'

  def test_initialize__valid_yaml__attributes(self,) -> None:
    instance = PrecheckValidator(self.yaml_data_valid)

    assert instance.parsed_yaml == yaml.safe_load(self.yaml_data_valid)
    assert instance.schema_definition == (
        Path(mac_maker.__file__).parent / "schemas" / "env_v1.json"
    )
    assert instance.schema == instance.load_json_file(
        instance.schema_definition
    )

  def test_initialize__invalid_yaml__raises_exception(self,) -> None:

    with pytest.raises(PrecheckValidationError) as exc:
      PrecheckValidator(self.yaml_data_invalid)

    assert str(exc.value) == PrecheckValidator.Messages.syntax_error

  def test_validate_config__valid_config__no_exception(self,) -> None:
    instance = PrecheckValidator(self.env_config_valid)

    instance.validate_config()

  def test_validate_config__invalid_config__raises_exception(self,) -> None:
    instance = PrecheckValidator(self.env_config_invalid)

    with pytest.raises(PrecheckValidationError) as exc:
      instance.validate_config()

    assert str(exc.value) == PrecheckValidator.Messages.syntax_error

  @mock.patch.dict(
      os.environ,
      {
          "USER": "niall",
          "JUMPCLOUD_CONNECT_KEY": "11",
      },
      clear=True,
  )
  def test_validate_environment__complete_env__returns_correct_value(
      self,
  ) -> None:
    instance = PrecheckValidator(self.env_config_valid)

    result = instance.validate_environment()

    assert result == {
        "is_valid": True,
        "violations": [],
    }

  @mock.patch.dict(os.environ, {"USER": "niall"}, clear=True)
  def test_validate_environment__partial_env__returns_correct_value(
      self,
  ) -> None:
    instance = PrecheckValidator(self.env_config_valid)
    var1 = instance.parsed_yaml[1]

    result = instance.validate_environment()

    assert result == {
        "is_valid": False,
        "violations": [instance.Messages.error_template.format(**var1)]
    }

  @mock.patch.dict(os.environ, {}, clear=True)
  def test_validate_environment__empty_env__returns_correct_value(
      self,
  ) -> None:
    instance = PrecheckValidator(self.env_config_valid)
    var0 = instance.parsed_yaml[0]
    var1 = instance.parsed_yaml[1]

    result = instance.validate_environment()

    assert result == {
        "is_valid":
            False,
        "violations":
            [
                instance.Messages.error_template.format(**var0),
                instance.Messages.error_template.format(**var1),
            ]
    }
