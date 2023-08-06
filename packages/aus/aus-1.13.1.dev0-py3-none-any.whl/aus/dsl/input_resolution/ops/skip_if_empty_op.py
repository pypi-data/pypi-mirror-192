"""Module for SkipIfEmpty operator."""

from typing import Sequence

from aus.dsl.input_resolution import resolver_op
from aus.orchestrator.portable.input_resolution import exceptions
from aus.utils import typing_utils


class SkipIfEmpty(
    resolver_op.ResolverOp,
    canonical_name='tfx.internal.SkipIfEmpty',
    arg_data_types=(resolver_op.DataType.ARTIFACT_MULTIMAP_LIST,),
    return_data_type=resolver_op.DataType.ARTIFACT_MULTIMAP_LIST,
):
    """SkipIfEmpty operator."""

    def apply(
            self,
            input_dict_list: Sequence[typing_utils.ArtifactMultiMap],
    ) -> Sequence[typing_utils.ArtifactMultiMap]:
        if not input_dict_list:
            raise exceptions.SkipSignal()
        return input_dict_list
