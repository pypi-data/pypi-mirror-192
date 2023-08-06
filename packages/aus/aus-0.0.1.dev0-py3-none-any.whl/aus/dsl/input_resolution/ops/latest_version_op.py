"""Module for LatestVersion operator."""

from typing import Sequence

from aus import types
from aus.dsl.input_resolution import resolver_op
from aus.dsl.input_resolution.ops import ops_utils


class LatestVersion(
    resolver_op.ResolverOp,
    canonical_name='tfx.LatestVersion',
    arg_data_types=(resolver_op.DataType.ARTIFACT_LIST,),
    return_data_type=resolver_op.DataType.ARTIFACT_LIST):
  """LatestVersion operator."""

  # The number of latest artifacts to return.
  n = resolver_op.Property(type=int, default=1)

  def apply(self,
            input_list: Sequence[types.Artifact]) -> Sequence[types.Artifact]:
    """Returns n artifacts with the latest version, ties broken by id.
    Note that the span property is only considered if all the artifacts with
    "version" as a PROPERTY also have "span" as a PROPERTY. In this case, then
    sorting will be done by (span, version, id), as opposed to just
    (version, id). Note that the artifacts will be sorted in ascending order.
    For example, consider 2 artifacts with:
      spans    = [0, 1]
      versions = [0, 0]
    In this case, LatestVersion(artifacts, n=1) will return the artifact with
    span = 1 and version = 0.
    LatestVersion(artifacts, n=2) will return the artifact with span = 0 and
    version = 0, and then the artifact with span = 1 and version = 0.
    Args:
      input_list: The list of Artifacts to parse.
    Returns:
      Artifacts with the n latest versions.
    """
    if not input_list:
      return []

    if self.n <= 0:
      raise ValueError(f'n must be > 0, but was set to {self.n}.')

    valid_artifacts = ops_utils.get_valid_artifacts(input_list,
                                                    ops_utils.VERSION_PROPERTY)
    if not valid_artifacts:
      return []

    # Consider span in the sorting only if all the artifacts have the span
    # PROPERTY.
    key = lambda a: (a.span, a.version, a.id)
    for artifact in valid_artifacts:
      if ('span' not in artifact.PROPERTIES or
          artifact.PROPERTIES['span'].type != types.artifacts.PropertyType.INT):
        key = lambda a: (a.version, a.id)
        break

    # Artifacts are sorted by key in ASCending order, with the last n returned.
    valid_artifacts.sort(key=key)
    return valid_artifacts[-self.n:]
