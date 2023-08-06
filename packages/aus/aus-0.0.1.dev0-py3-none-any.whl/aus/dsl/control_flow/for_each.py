"""Module for `ForEach` context manager."""

from typing import Union, cast, Any

from aus.dsl.context_managers import dsl_context_manager
from aus.dsl.control_flow import for_each_internal
from aus.dsl.input_resolution import resolver_function
from aus.dsl.input_resolution.ops import ops
from aus.types import channel as channel_types

# Re-export name for backward compatibility.
ForEachContext = for_each_internal.ForEachContext


# ForEach for single channel uses resolver function (which has Unnest).
@resolver_function.resolver_function(unwrap_dict_key='out')
def _for_each_impl(channel: channel_types.BaseChannel):
  return ops.Unnest({'out': channel}, key='out')


@_for_each_impl.output_type_inferrer
def _for_each_output_type(channel: channel_types.BaseChannel):
  return {'out': channel.type}


class ForEach(dsl_context_manager.DslContextManager[Any]):
  """ForEach context manager.
  ForEach context manager is a declarative version of For loop in a pipeline
  defintion (in DSL). When some TFX components generate more than one artifacts,
  or resolver function returns a multiple inputs, ForEach is used to handle
  each artifact or input dictionary individually.
  ```python
  example_gen = BufferedExampleGen()
  # example_gen.outputs['examples'] containing N artifacts.
  with ForEach(example_gen.outputs['examples']) as examples:
    trainer = Trainer(
        examples=examples,  # instead of using example_gen.outputs['examples'].
        ...)
  ```
  In the above example, only a single Trainer component is declared in the
  pipeline, but it can be executed multiple times (or even zero time) in a
  single pipeline run depending on the number of output artifacts that
  example_gen has generated.
  ResolverFunction can also output a loopable which can be accessed from the
  handle as a dict of channels:
  ```python
  evaluator_inputs = sliding_window(examples=examples)
  with ForEach(evaluator_inputs) as each_input:
    evaluator = Evaluator(
        examples=each_input['examples'],
        model=trainer.outputs['model'],
        ...
    )
  ```
  """

  def __init__(self, loopable: Union[channel_types.BaseChannel,
                                     for_each_internal.Loopable]):
    super().__init__()
    if isinstance(loopable, channel_types.BaseChannel):
      self._loopable = cast(
          for_each_internal.Loopable,
          _for_each_impl(cast(channel_types.BaseChannel, loopable)))
    elif isinstance(loopable, for_each_internal.Loopable):
      self._loopable = loopable
    else:
      raise ValueError(f'{loopable} cannot be used as a ForEach argument.')

  def create_context(self) -> ForEachContext:
    return for_each_internal.ForEachContext()

  # TODO(b/266112670): Return value should be a generic type (T) once the
  # Loopable type become generic as well (Loopable[T]).
  def enter(self, context: ForEachContext) -> Any:  # pytype: disable=signature-mismatch  # overriding-parameter-type-checks
    return self._loopable.get_loop_var(context)
