import knime.extension as knext

from util.port_objects import (
    PositionPortObject,
    PositionPortObjectSpec,
    AttributePortObject,
    AttributePortObjectSpec,
    NetworkPortObject,
    NetworkPortObjectSpec,
)

position_port_type = knext.port_type(
    name="Position Port Type",
    object_class=PositionPortObject,
    spec_class=PositionPortObjectSpec,
)

attribute_port_type = knext.port_type(
    name="Attribute Port Type",
    object_class=AttributePortObject,
    spec_class=AttributePortObjectSpec,
)

network_port_type = knext.port_type(
    name="Network Port Type",
    object_class=NetworkPortObject,
    spec_class=NetworkPortObjectSpec,
)
