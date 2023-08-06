"""Stub for pre-rename `tfx.dsl.components.base.base_component`."""

from aus.dsl.widgets.base import base_component
from aus.utils import deprecation_utils

BaseComponent = deprecation_utils.deprecated_alias(  # pylint: disable=invalid-name
    deprecated_name='tfx.components.base.base_component.BaseComponent',
    name='tfx.dsl.components.base.base_component.BaseComponent',
    func_or_class=base_component.BaseComponent)
