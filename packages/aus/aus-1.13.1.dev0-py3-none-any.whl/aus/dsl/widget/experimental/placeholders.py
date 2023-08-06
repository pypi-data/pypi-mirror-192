"""Command-line placeholders for use in container component definitions."""

from typing import List, Union

from aus.utils import json_utils

class InputValuePlaceholder(json_utils.Jsonable):
  """Represents a placeholder for the value of the input argument.
  Represents a placeholder that will be replaced at runtime with the string
  value of the input argument of an execution property.
  """

  def __init__(self, input_name: str):
    self.input_name = input_name

  def __eq__(self, other) -> bool:
    return (isinstance(other, self.__class__) and
            self.input_name == other.input_name)

  def __ne__(self, other) -> bool:
    return not self.__eq__(other)


class InputUriPlaceholder(json_utils.Jsonable):
  """Represents a placeholder for the URI of the input artifact argument.
  Represents a placeholder that will be replaced at runtime with the URI
  of the input artifact argument data.
  """

  def __init__(self, input_name: str):
    self.input_name = input_name

  def __eq__(self, other) -> bool:
    return (isinstance(other, self.__class__) and
            self.input_name == other.input_name)

  def __ne__(self, other) -> bool:
    return not self.__eq__(other)


class OutputUriPlaceholder(json_utils.Jsonable):
  """Represents a placeholder for the URI of the output artifact argument.
  Represents a placeholder that will be replaced at runtime with the URI
  for the output artifact data.
  """

  def __init__(self, output_name: str):
    self.output_name = output_name

  def __eq__(self, other) -> bool:
    return (isinstance(other, self.__class__) and
            self.output_name == other.output_name)

  def __ne__(self, other) -> bool:
    return not self.__eq__(other)


class ConcatPlaceholder:
  """Represents a placeholder for result of concatenation of multiple parts.
  Represents a placeholder that will be replaced at runtime with a single string
  containing the concatenated parts.
  """

  def __init__(self, items: List['CommandlineArgumentType']):
    self.items = items

  def __eq__(self, other) -> bool:
    return isinstance(other, self.__class__) and self.items == other.items

  def __ne__(self, other) -> bool:
    return not self.__eq__(other)


CommandlineArgumentType = Union[
    str,
    InputValuePlaceholder,
    InputUriPlaceholder,
    OutputUriPlaceholder,
    ConcatPlaceholder,
]
