"""Test helpers for pytest parametrize."""

from typing import Any, List, Tuple

import pytest
from _pytest.mark import ParameterSet


def named_parameters(*args: Tuple[Any, ...], name: int) -> List[ParameterSet]:
  """Extract a test id from a pytest parameter set."""

  return [pytest.param(*argset, id=argset[name]) for argset in args]
