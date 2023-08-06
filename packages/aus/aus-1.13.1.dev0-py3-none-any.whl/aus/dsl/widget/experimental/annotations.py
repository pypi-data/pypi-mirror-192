"""TFX Python function component type annotations.
Experimental. No backwards compatibility guarantees.
"""

import inspect
from typing import Any, Type, Union

from aus.dsl.widget.experimental import json_compat
from aus.types import artifact

try:
    import apache_beam as beam  # pytype: disable=import-error  # pylint: disable=g-import-not-at-top

    _BeamPipeline = beam.Pipeline
except ModuleNotFoundError:
    beam = None
    _BeamPipeline = Any


class _ArtifactGenericMeta(type):
    """Metaclass for _ArtifactGeneric, to enable class indexing."""

    def __getitem__(cls: Type['_ArtifactGeneric'],
                    params: Type[artifact.Artifact]):
        """Metaclass method allowing indexing class (`_ArtifactGeneric[T]`)."""
        return cls._generic_getitem(params)  # pytype: disable=attribute-error


class _ArtifactGeneric(metaclass=_ArtifactGenericMeta):
    """A generic that takes a Type[tfx.types.Artifact] as its single argument."""

    def __init__(  # pylint: disable=invalid-name
            self,
            artifact_type: Type[artifact.Artifact],
            _init_via_getitem=False):
        if not _init_via_getitem:
            class_name = self.__class__.__name__
            raise ValueError(
                ('%s should be instantiated via the syntax `%s[T]`, where T is a '
                 'subclass of tfx.types.Artifact.') % (class_name, class_name))
        self.type = artifact_type

    @classmethod
    def _generic_getitem(cls, params):
        """Return the result of `_ArtifactGeneric[T]` for a given type T."""
        # Check that the given parameter is a concrete (i.e. non-abstract) subclass
        # of `tfx.types.Artifact`.
        if (inspect.isclass(params) and issubclass(params, artifact.Artifact) and
                params.TYPE_NAME):
            return cls(params, _init_via_getitem=True)
        else:
            class_name = cls.__name__
            raise ValueError(
                ('Generic type `%s[T]` expects the single parameter T to be a '
                 'concrete subclass of `tfx.types.Artifact` (got %r instead).') %
                (class_name, params))

    def __repr__(self):
        return '%s[%s]' % (self.__class__.__name__, self.type)


class _PrimitiveTypeGenericMeta(type):
    """Metaclass for _PrimitiveTypeGeneric, to enable primitive type indexing."""

    def __getitem__(cls: Type['_PrimitiveTypeGeneric'],
                    params: Type[Union[int, float, str, bool]]):
        """Metaclass method allowing indexing class (`_PrimitiveTypeGeneric[T]`)."""
        return cls._generic_getitem(params)  # pytype: disable=attribute-error


class _PrimitiveTypeGeneric(metaclass=_PrimitiveTypeGenericMeta):
    """A generic that takes a primitive type as its single argument."""

    def __init__(  # pylint: disable=invalid-name
            self,
            artifact_type: Type[Union[int, float, str, bool, bytes]],
            _init_via_getitem=False):
        if not _init_via_getitem:
            class_name = self.__class__.__name__
            raise ValueError(
                ('%s should be instantiated via the syntax `%s[T]`, where T is '
                 '`int`, `float`, `str`, or `bool`.') %
                (class_name, class_name))
        self._type = artifact_type

    @classmethod
    def _generic_getitem(cls, params):
        """Return the result of `_PrimitiveTypeGeneric[T]` for a given type T."""
        # Check that the given parameter is a primitive type.
        if (inspect.isclass(params) and params in (int, float, str, bool, bytes) or
                json_compat.is_json_compatible(params)):
            return cls(params, _init_via_getitem=True)
        else:
            class_name = cls.__name__
            raise ValueError(
                ('Generic type `%s[T]` expects the single parameter T to be '
                 '`int`, `float`, `str`, `bool` or JSON-compatible types '
                 '(Dict[str, T], List[T]) (got %r instead).') %
                (class_name, params))

    def __repr__(self):
        return '%s[%s]' % (self.__class__.__name__, self._type)

    @property
    def type(self):
        return self._type


class _PipelineTypeGenericMeta(type):
    """Metaclass for _PipelineTypeGeneric."""

    def __getitem__(cls: Type['_PipelineTypeGeneric'],
                    params: Type[_BeamPipeline]):
        """Metaclass method allowing indexing class (`_PipelineTypeGeneric[T]`)."""
        return cls._generic_getitem(params)  # pytype: disable=attribute-error


class _PipelineTypeGeneric(
    metaclass=_PipelineTypeGenericMeta):
    """A generic that takes a beam.Pipeline as its single argument."""

    def __init__(  # pylint: disable=invalid-name
            self,
            artifact_type: Type[_BeamPipeline],
            _init_via_getitem=False):
        if not _init_via_getitem:
            class_name = self.__class__.__name__
            raise ValueError(
                ('%s should be instantiated via the syntax `%s[T]`, where T is '
                 '`beam.Pipeline`.') %
                (class_name, class_name))
        self._type = artifact_type

    @classmethod
    def _generic_getitem(cls, params):
        """Return the result of `_PrimitiveTypeGeneric[T]` for a given type T."""
        # Check that the given parameter is a primitive type.
        if inspect.isclass(params) and params in (_BeamPipeline,):
            return cls(params, _init_via_getitem=True)
        else:
            class_name = cls.__name__
            raise ValueError(
                ('Generic type `%s[T]` expects the single parameter T to be '
                 '`beam.Pipeline`, got %r instead.') %
                (class_name, params))

    def __repr__(self):
        return '%s[%s]' % (self.__class__.__name__, self._type)

    @property
    def type(self):
        return self._type


# Typehint annotations for component authoring.


class InputArtifact(_ArtifactGeneric):
    """Input artifact object type annotation."""
    pass


class OutputArtifact(_ArtifactGeneric):
    """Output artifact object type annotation."""
    pass


class Parameter(_PrimitiveTypeGeneric):
    """Component parameter type annotation."""
    pass


class BeamComponentParameter(_PipelineTypeGeneric):
    """Component parameter type annotation."""
    pass


# TODO(ccy): potentially make this compatible `typing.TypedDict` in
# Python 3.8, to allow for component return value type checking.
class OutputDict:
    """Decorator declaring component executor function outputs."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
