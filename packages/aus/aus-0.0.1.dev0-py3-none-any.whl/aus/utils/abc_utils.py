"""Utilies for abstract classes."""

import abc
from typing import Any


def abstract_property() -> Any:
  """Returns an abstract property for use in an ABC abstract class."""
  return abc.abstractmethod(lambda: None)
