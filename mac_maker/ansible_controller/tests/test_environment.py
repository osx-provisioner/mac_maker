"""Test the Environment class."""
import os
from logging import Logger
from unittest import TestCase, mock

from ...utilities import filesystem, state
from .. import environment

ENV_MODULE = environment.__name__


def mock_environment(**environment_variables):
  return mock.patch.dict(os.environ, environment_variables)


class TestEnvironmentClass(TestCase):
  """Test the Environment class."""

  def setUp(self):
    self.mock_root = ""
    self.filesystem = filesystem.FileSystem(self.mock_root)
    self.state = state.State()
    self.mock_state = self.state.state_generate(self.filesystem)
    self.environment = environment.Environment(self.mock_state)

  def test_init(self):

    self.assertIsInstance(
        self.environment.log,
        Logger,
    )
    self.assertEqual(
        self.environment.state,
        self.state.state_generate(self.filesystem),
    )
    self.assertDictEqual(
        self.environment.env,
        {},
    )

  @mock_environment()
  def test_setup_clean_environment(self):

    self.environment.setup()

    self.assertDictEqual(
        self.environment.env, {
            'ANSIBLE_ROLES_PATH': self.mock_state['roles_path'][0],
            'ANSIBLE_COLLECTIONS_PATH': self.mock_state['collections_path'][0],
        }
    )

    for key, value in self.environment.env.items():
      self.assertEqual(os.environ[key], value)

  @mock_environment()
  def test_setup_clean_environment_multiple(self):
    self.mock_state['roles_path'].append('/non/existent/1')
    self.mock_state['collections_path'].append('/non/existent/2')

    self.environment.setup()

    self.assertDictEqual(
        self.environment.env, {
            'ANSIBLE_ROLES_PATH':
                ":".join(self.mock_state['roles_path']),
            'ANSIBLE_COLLECTIONS_PATH':
                ":".join(self.mock_state['collections_path']),
        }
    )

    for key, value in self.environment.env.items():
      self.assertEqual(os.environ[key], value)

  @mock_environment(
      ANSIBLE_ROLES_PATH='/non/existent/01:/non/existent/02',
      ANSIBLE_COLLECTIONS_PATH='/non/existent/03:/non/existent/04',
  )
  def test_setup_clean_environment_existing(self):
    self.environment.setup()

    self.assertDictEqual(
        self.environment.env, {
            'ANSIBLE_ROLES_PATH':
                ":".join(
                    self.mock_state['roles_path'] + [
                        '/non/existent/01',
                        '/non/existent/02',
                    ]
                ),
            'ANSIBLE_COLLECTIONS_PATH':
                ":".join(
                    self.mock_state['collections_path'] + [
                        '/non/existent/03',
                        '/non/existent/04',
                    ]
                ),
        }
    )

    for key, value in self.environment.env.items():
      self.assertEqual(os.environ[key], value)
