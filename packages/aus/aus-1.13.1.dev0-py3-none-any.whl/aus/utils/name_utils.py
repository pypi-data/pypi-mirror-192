"""Utility related to python object names."""
import importlib
from typing import Any, Sequence


def _is_valid_name(value: str) -> bool:
  return (isinstance(value, str) and
          all(token.isidentifier() for token in value.split('.')))


def _get_nested_attr(obj: Any, attrs: Sequence[str]):
  if len(attrs) == 1:
    return getattr(obj, attrs[0])
  else:
    attr, *rest = attrs
    if not hasattr(obj, attr):
      raise AttributeError(f'{obj} does not have {attr} attribute.')
    return _get_nested_attr(getattr(obj, attr), rest)


def _get_qualified_name(value: Any) -> str:
  if hasattr(value, '__qualname__'):
    return value.__qualname__
  elif hasattr(value, '__name__'):
    return value.__name__
  raise ValueError(f'{value} does not have a name.')


def get_full_name(value: Any, strict_check: bool = True) -> str:
  """Get fully qualified name of the given class or function."""
  if not hasattr(value, '__module__') or not hasattr(value, '__name__'):
    raise ValueError(f'{value} does not have a name.')
  name = _get_qualified_name(value)
  if strict_check:
    if not _is_valid_name(name):
      # Locally defined classes have invalid name (foo.<local>.MyClass)
      raise ValueError(f'{value} does not have a qualified name.')
    mod = importlib.import_module(value.__module__)
    try:
      _get_nested_attr(mod, name.split('.'))
    except AttributeError as e:
      # Dynamically created classes is not importable and should not be accessed
      # by the full_name.
      raise ValueError(f'{value} is not importable.') from e
  return f'{value.__module__}.{name}'


def resolve_full_name(full_name: str) -> Any:
  """Resolves reference (class, function, value, etc.) of the full_name."""
  if not _is_valid_name(full_name):
    raise ValueError(f'{full_name!r} is not a valid name.')
  segments = full_name.split('.')
  errors = []
  for i in range(len(segments) - 1, 0, -1):
    module_name = '.'.join(segments[:i])
    try:
      mod = importlib.import_module(module_name)
      result = _get_nested_attr(mod, segments[i:])
      break
    except (ImportError, AttributeError) as e:
      errors.append(e)
      continue
  else:
    raise ValueError(f'Cannot find {full_name}: {errors}')
  return result
