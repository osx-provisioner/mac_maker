"""Test harness for cases requiring a GitHub Repository."""

import unittest

from ...cli import Jobs


class GitTestHarness(unittest.TestCase):
  """Test fixtures for the click CLI."""

  def setUp(self) -> None:
    self.repo_name = "panic"
    self.org_name = "grocerypanic"
    self.repository_http_url = (
        f"https://github.com/{self.org_name}/"
        f"{self.repo_name}.git"
    )
    self.repository_ssh_url = (
        f"git@github.com:{self.org_name}/{self.repo_name}.git"
    )
    self.jobs = Jobs()
