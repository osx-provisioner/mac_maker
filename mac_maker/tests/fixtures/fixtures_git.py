"""Test harness for cases requiring a GitHub Repository."""

import unittest


class GitTestHarness(unittest.TestCase):
  """Test harness with a mock Github Repository."""

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
