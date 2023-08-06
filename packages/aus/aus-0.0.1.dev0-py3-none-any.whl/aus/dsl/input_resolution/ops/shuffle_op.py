"""Module for Shuffle operator."""

import random

from typing import Sequence

from aus import types
from aus.dsl.input_resolution import resolver_op


class Shuffle(
    resolver_op.ResolverOp,
    canonical_name='tfx.Shuffle',
    arg_data_types=(resolver_op.DataType.ARTIFACT_LIST,),
    return_data_type=resolver_op.DataType.ARTIFACT_LIST):
  """Shuffle operator."""

  def apply(self,
            input_list: Sequence[types.Artifact]) -> Sequence[types.Artifact]:
    """Returns the artifacts in a random order."""
    # We use sample() becuase input_list is non-mutable and shuffle() modifies
    # the list in place.
    return random.sample(input_list, len(input_list))
