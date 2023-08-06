"""Module for Unnest operator."""

from aus.dsl.input_resolution import resolver_op
from aus.orchestrator.portable.input_resolution import exceptions
from aus.utils import typing_utils


class Unnest(
    resolver_op.ResolverOp,
    canonical_name='tfx.internal.Unnest',
    arg_data_types=(resolver_op.DataType.ARTIFACT_MULTIMAP,),
    return_data_type=resolver_op.DataType.ARTIFACT_MULTIMAP_LIST,
):
  """Unnest operator.
  Unnest operator split a *`key` channel* of multiple artifacts into multiple
  dicts each with a channel with single artifact. Pseudo code example:
      Unnest({x: [x1, x2, x3]}, key=x)
        = [{x: [x1]}, {x: [x2]}, {x: [x3]}]
  For channels other than key channel remains the same. Pseudo code example:
      Unnest({x: [x1, x2, x3], y: [y1]}, key=x)
        = [{x: [x1], y: [y1]}, {x: [x2], y: [y1]}, {x: [x3], y: [y1]}]
  """
  key = resolver_op.Property(type=str)

  def apply(self, input_dict: typing_utils.ArtifactMultiMap):
    if self.key not in input_dict:
      raise exceptions.FailedPreconditionError(
          f'Input dict does not contain the key {self.key}. '
          f'Available: {list(input_dict.keys())}')

    main_channel = input_dict.get(self.key)
    rest = {k: v for k, v in input_dict.items() if k != self.key}
    result = []
    for main_artifact in main_channel:
      result.append({self.key: [main_artifact], **rest})
    return result
