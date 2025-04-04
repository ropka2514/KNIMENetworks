import knime.extension as knext

import networks_ext
from util.port_types import (
    NetworkPortObject,
    NetworkPortObjectSpec,
    network_port_type,
)


@knext.node(
    name="Network to Table",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_port(
    name="Input Network",
    description="Input network to convert to table.",
    port_type=network_port_type,
)
@knext.output_table(
    name="Output Table",
    description="Output table with network data.",
)
class NetworkTableNode:
    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema: NetworkPortObjectSpec,
    ) -> knext.Schema:
        # ktype1 = knext.string()
        # ktype2 = input_schema.weight_column.ktype
        # return knext.Schema([ktype1,ktype1, ktype2],[input_schema.source_label, input_schema.target_label, input_schema.weight_label])
        return None

    def execute(self, context, input):
        network = input.get_network()

        return network
