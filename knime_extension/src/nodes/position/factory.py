import knime.extension as knext
import networks_ext
from util.position_algorithms import create_positions
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
    PositionPortObject,
    PositionPortObjectSpec,
)
from util.port_types import (
    network_port_type,
    position_port_type,
    attribute_port_type,
)


class StringMethodOptions(knext.EnumParameterOptions):
    BINARY = (
        "Binary",
        "Treat string relation values as binary relation. Loss of information may occur.",
    )
    ONE_HOT = (
        "One-Hot",
        "One-Hot encoding for string relation values. (Split Into Layers)",
    )


@knext.parameter_group(label="Network Position Settings")
class NetworkPositionSettings:
    string_method = knext.EnumParameter(
        label="String Method",
        description="Select the method to compute string positions.",
        enum=StringMethodOptions,
        default_value=StringMethodOptions.BINARY.name,
    )


@knext.node(
    name="Position Creation",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/position.png",
)
@knext.input_port_group(
    name="Input Network",
    description="Input network to compute positions.",
    port_type=network_port_type,
)
@knext.input_port_group(
    name="Input Attributes",
    description="Input attributes to compute positions.",
    port_type=attribute_port_type,
)
@knext.output_port(
    name="Output Positions",
    description="Position object created from the network.",
    port_type=position_port_type,
)
class NetworkPositionNode:
    settings = NetworkPositionSettings()

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        network_schema: list[NetworkPortObjectSpec],
        attribute_schema: list[PositionPortObjectSpec],
    ) -> PositionPortObjectSpec:
        source_label = network_schema[0].source_label

        return PositionPortObjectSpec(
            node_column=source_label,
        )

    def execute(
        self, context, input_networks: list[NetworkPortObject], input_attributes: list[PositionPortObject] = []
    ) -> PositionPortObject:
        return create_positions(input_networks, input_attributes, self.settings.string_method)
