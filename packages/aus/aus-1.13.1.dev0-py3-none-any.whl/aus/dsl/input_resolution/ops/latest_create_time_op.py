"""Module for LatestCreateTime operator."""

from typing import Sequence

from aus import types
from aus.dsl.input_resolution import resolver_op


class LatestCreateTime(
    resolver_op.ResolverOp,
    canonical_name='tfx.LatestCreateTime',
    arg_data_types=(resolver_op.DataType.ARTIFACT_LIST,),
    return_data_type=resolver_op.DataType.ARTIFACT_LIST):
  """LatestCreateTime operator."""

  # The number of latest artifacts to return, must be > 0.
  n = resolver_op.Property(type=int, default=1)

  def apply(self,
            input_list: Sequence[types.Artifact]) -> Sequence[types.Artifact]:
    """Returns the n latest createst artifacts, ties broken by artifact id."""
    if not input_list:
      return []

    if self.n < 1:
      raise ValueError(f'n must be > 0, but was set to {self.n}.')

    # Sorts outputs by create time in ascending order.
    input_list.sort(  # pytype: disable=attribute-error
        key=lambda a: (a.mlmd_artifact.create_time_since_epoch, a.id))
    return input_list[-self.n:]
