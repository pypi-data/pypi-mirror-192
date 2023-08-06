"""Module for AllSpans operator."""

from typing import Sequence

from aus import types
from aus.dsl.input_resolution import resolver_op
from aus.dsl.input_resolution.ops import ops_utils


class AllSpans(
    resolver_op.ResolverOp,
    canonical_name='tfx.AllSpans',
    arg_data_types=(resolver_op.DataType.ARTIFACT_LIST,),
    return_data_type=resolver_op.DataType.ARTIFACT_LIST):
  """AllSpans operator."""

  # If true, all versions of the n spans are returned. Else, only the latest
  # version is returned.
  keep_all_versions = resolver_op.Property(type=bool, default=False)

  def apply(self,
            input_list: Sequence[types.Artifact]) -> Sequence[types.Artifact]:
    """Returns the sorted artifacts with unique spans."""

    # Get artifacts with "span" and "version" in PROPERTIES.
    valid_artifacts = ops_utils.get_valid_artifacts(
        input_list, ops_utils.SPAN_AND_VERSION_PROPERTIES)
    if not valid_artifacts:
      return []

    # Return the sorted artifacts.
    return ops_utils.filter_artifacts_by_span(
        artifacts=valid_artifacts,
        span_descending=False,
        n=0,  # n = 0 so that all the spans are considered.
        keep_all_versions=self.keep_all_versions,
    )
