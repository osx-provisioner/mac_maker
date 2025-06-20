"""Test helpers for pytest parametrize."""

from typing import Any, Callable, List, Optional, Tuple

import pytest
from _pytest.mark import ParameterSet


def named_parameters(*args: Tuple[Any, ...], name: int) -> List[ParameterSet]:
  """Extract a test id from a pytest parameter set."""

  return [pytest.param(*argset, id=argset[name]) for argset in args]


def templated_ids(
    template: str,
    transformation: Optional[Callable[[Any], str]] = None,
) -> Callable[[Any], str]:
  """Create a test id function from a template string."""

  def templater(arg: Any) -> str:
    if transformation:
      arg = transformation(arg)
    return template.format(arg)

  return templater
