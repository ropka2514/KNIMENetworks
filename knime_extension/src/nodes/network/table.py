import knime.extension as knext

import networks_ext
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)
from util.port_types import (
    network_port_type,
)

@knext.node(
    name="Network to Table",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.network_category,
    icon_path="icons/to-table.png",
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
        return None

    def execute(self, context, input: NetworkPortObject) -> knext.Table:
        network = input.get_network()

        return knext.Table.from_pandas(network)
