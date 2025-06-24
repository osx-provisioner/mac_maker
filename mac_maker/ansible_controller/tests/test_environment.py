"""Test the AnsibleEnvironment class."""
import os
from logging import Logger
from unittest import mock

from mac_maker.ansible_controller import environment, spec

TypeMockDict = mock._patch_dict  # pylint: disable=protected-access


class TestAnsibleEnvironment:
  """Test the AnsibleEnvironment class."""

  @staticmethod
  def mock_environment(**environment_variables: str) -> TypeMockDict:
    return mock.patch.dict(os.environ, environment_variables)

  def test_initialize__attributes(
      self,
      ansible_environment: environment.AnsibleEnvironment,
      global_spec_mock: spec.Spec,
  ) -> None:
    assert isinstance(ansible_environment.log, Logger)
    assert ansible_environment.spec == global_spec_mock
    assert ansible_environment.env == {}

  @mock_environment()
  def test_setup__clean_env__single_sources__correct_instance_dictionary(
      self,
      ansible_environment: environment.AnsibleEnvironment,
      global_spec_mock: spec.Spec,
  ) -> None:
    global_spec_mock.roles_path = ['/non/existent/1']
    global_spec_mock.collections_path = ['/non/existent/2']

    ansible_environment.setup()

    assert ansible_environment.env == {
        'ANSIBLE_ROLES_PATH': global_spec_mock.roles_path[0],
        'ANSIBLE_COLLECTIONS_PATH': global_spec_mock.collections_path[0],
    }

  @mock_environment()
  def test_setup__clean_env__single_sources__correct_env_vars(
      self,
      ansible_environment: environment.AnsibleEnvironment,
      global_spec_mock: spec.Spec,
  ) -> None:
    global_spec_mock.roles_path = ['/non/existent/1']
    global_spec_mock.collections_path = ['/non/existent/2']

    ansible_environment.setup()

    for key, value in ansible_environment.env.items():
      assert os.environ[key] == value

  @mock_environment()
  def test_setup__clean_env__multiple_sources__correct_instance_dictionary(
      self,
      ansible_environment: environment.AnsibleEnvironment,
      global_spec_mock: spec.Spec,
  ) -> None:
    global_spec_mock.roles_path.append('/non/existent/1')
    global_spec_mock.collections_path.append('/non/existent/2')

    ansible_environment.setup()

    assert ansible_environment.env == {
        'ANSIBLE_ROLES_PATH': ":".join(global_spec_mock.roles_path),
        'ANSIBLE_COLLECTIONS_PATH': ":".join(global_spec_mock.collections_path),
    }

  @mock_environment()
  def test_setup__clean_env__multiple_sources__correct_env_vars(
      self,
      ansible_environment: environment.AnsibleEnvironment,
      global_spec_mock: spec.Spec,
  ) -> None:
    global_spec_mock.roles_path.append('/non/existent/1')
    global_spec_mock.collections_path.append('/non/existent/2')

    ansible_environment.setup()

    for key, value in ansible_environment.env.items():
      assert os.environ[key] == value

  @mock_environment(
      ANSIBLE_ROLES_PATH='/non/existent/01:/non/existent/02',
      ANSIBLE_COLLECTIONS_PATH='/non/existent/03:/non/existent/04',
  )
  def test_setup__existing_env__multiple_sources__correct_instance_dictionary(
      self,
      ansible_environment: environment.AnsibleEnvironment,
      global_spec_mock: spec.Spec,
  ) -> None:
    ansible_environment.setup()

    assert ansible_environment.env == {
        'ANSIBLE_ROLES_PATH':
            ":".join(
                global_spec_mock.roles_path + [
                    '/non/existent/01',
                    '/non/existent/02',
                ]
            ),
        'ANSIBLE_COLLECTIONS_PATH':
            ":".join(
                global_spec_mock.collections_path + [
                    '/non/existent/03',
                    '/non/existent/04',
                ]
            ),
    }

  @mock_environment(
      ANSIBLE_ROLES_PATH='/non/existent/01:/non/existent/02',
      ANSIBLE_COLLECTIONS_PATH='/non/existent/03:/non/existent/04',
  )
  def test_setup__existing_env__multiple_sources__correct_env_vars(
      self,
      ansible_environment: environment.AnsibleEnvironment,
  ) -> None:
    ansible_environment.setup()

    for key, value in ansible_environment.env.items():
      assert os.environ[key] == value
