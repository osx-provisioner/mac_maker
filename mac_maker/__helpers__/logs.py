"""Test helpers for mac_maker."""

from logging import LogRecord
from typing import List


def decode_logs(logs: List[LogRecord]) -> List[str]:
  """Translate LogRecords into testable strings."""

  return [
      f'{entry.levelname}:{entry.name}:{entry.getMessage()}' for entry in logs
  ]
