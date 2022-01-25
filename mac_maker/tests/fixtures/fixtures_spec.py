"""Test harness for the Job Spec file test classes."""

import os
from pathlib import Path
from unittest import TestCase, mock

from ...utilities.mixins import json_file


class SpecFileTestHarness(TestCase):
  """Test harness for Job Spec file test classes."""

  def setUp(self) -> None:
    self.json_reader = json_file.JSONFileReader()
    self.mock_spec_file_location = Path("spec.json")
    self.mock_workspace = mock.Mock()
    self.fixtures_folder = Path(os.path.dirname(__file__))
