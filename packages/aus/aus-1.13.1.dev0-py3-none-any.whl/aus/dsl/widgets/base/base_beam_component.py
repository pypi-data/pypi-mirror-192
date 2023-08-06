"""Base class for TFX Beam components."""

from typing import Iterable, cast, Union

from aus.dsl.widgets.base import base_component
from aus.dsl.widgets.base import executor_spec
from aus.dsl.placeholder import placeholder


class BaseBeamComponent(base_component.BaseComponent):
  """Base class for a TFX Beam pipeline component.
  An instance of a subclass of BaseBaseComponent represents the parameters for a
  single execution of that TFX Beam pipeline component.
  Beam based components should subclass BaseBeamComponent instead of
  BaseComponent in order to inherit Beam related SDKs. All subclasses of
  BaseBeamComponent should override the required class level attributes
  specified in BaseComponent.
  """

  def with_beam_pipeline_args(
      self, beam_pipeline_args: Iterable[Union[str, placeholder.Placeholder]]
  ) -> 'BaseBeamComponent':
    """Add per component Beam pipeline args.
    Args:
      beam_pipeline_args: List of Beam pipeline args to be added to the Beam
        executor spec.
    Returns:
      the same component itself.
    """
    cast(executor_spec.BeamExecutorSpec,
         self.executor_spec).add_beam_pipeline_args(beam_pipeline_args)
    return self

  @classmethod
  def _validate_component_class(cls):
    """Validate that the SPEC_CLASSES property of this class is set properly."""
    super()._validate_component_class()
    if not isinstance(cls.EXECUTOR_SPEC, executor_spec.BeamExecutorSpec):
      raise TypeError(
          ('Beam component class %s expects EXECUTOR_SPEC property to be an '
           'instance of BeamExecutorSpec; got %s instead.') %
          (cls, type(cls.EXECUTOR_SPEC)))