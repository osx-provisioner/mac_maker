"""Test helpers for pytest parametrize."""

from typing import Any, Callable, List, Optional, Tuple

import pytest
from _pytest.mark import ParameterSet


def named_parameters(
    *args: Tuple[Any, ...],
    names: List[int],
) -> List[ParameterSet]:
  """Extract a test id from a pytest parameter set."""

  return [
      pytest.param(
          *argset,
          id=str(*[argset[selected] for selected in names]),
      ) for argset in args
  ]


def templated_ids(
    template: str,
    transformation: Optional[Callable[[Any], str]] = None,
) -> Callable[[Any], str]:
  """Create a test id function from a template string."""

  def templater(*args: Any) -> str:
    if transformation:
      args = tuple(transformation(arg) for arg in args)
    return template.format(*args)

  return templater


def templated_parameters(
    *args: Tuple[Any, ...],
    names: List[int],
    template: str,
    transformation: Optional[Callable[[Any], str]] = None,
) -> List[ParameterSet]:
  """Create a test id function from a template string."""

  templater = templated_ids(template, transformation)

  return [
      pytest.param(
          *argset,
          id=templater(*[argset[selected] for selected in names]),
      ) for argset in args
  ]
