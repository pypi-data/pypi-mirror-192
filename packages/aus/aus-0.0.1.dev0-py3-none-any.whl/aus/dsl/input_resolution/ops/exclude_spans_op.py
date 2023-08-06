"""Module for ExcludeSpans operator."""

from typing import Sequence

from aus import types
from aus.dsl.input_resolution import resolver_op
from aus.dsl.input_resolution.ops import ops_utils


class ExcludeSpans(
    resolver_op.ResolverOp,
    canonical_name='tfx.ExcludeSpans',
    arg_data_types=(resolver_op.DataType.ARTIFACT_LIST,),
    return_data_type=resolver_op.DataType.ARTIFACT_LIST,
):
  """ExcludeSpans operator."""

  # The span numbers to exclude.
  denylist = resolver_op.Property(type=Sequence[int], default=[])

  def apply(
      self,
      input_list: Sequence[types.Artifact],
  ) -> Sequence[types.Artifact]:
    """Returns artifacts with spans not in denylist.
    Corresponds to exclude_span_numbers in RangeConfig in TFX.
    For example, if the artifacts have spans [1, 2, 2, 4], and
    denylist = [1, 2], then only the artifact [4] will be returned.
    Args:
      input_list: The list of Artifacts to parse.
    Returns:
      Artifacts with spans not in denylist.
    """
    valid_artifacts = ops_utils.get_valid_artifacts(input_list,
                                                    ops_utils.SPAN_PROPERTY)

    # Only return artifacts that do not have spans in denylist.
    return [a for a in valid_artifacts if a.span not in set(self.denylist)]
