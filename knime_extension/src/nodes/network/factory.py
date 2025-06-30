import knime.extension as knext

import networks_ext
from util.network_algorithms import create_network
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)
from util.port_types import (
    network_port_type,
)

@knext.parameter_group(label="Network Settings")
class NetworkSettings:
    source_label = knext.ColumnParameter(
        label="Source nodes",
        description="Select the column with the source nodes.",
    )
    target_label = knext.ColumnParameter(
        label="Target nodes",
        description="Select the column with the target nodes.",
    )
    weight_label = knext.ColumnParameter(
        label="Values",
        description="Select the column with the values.",
    )
    two_mode = knext.BoolParameter(
        label="Two-mode",
        description="Select if the network is two-mode.",
        default_value=False,
    )
    symmetric = knext.BoolParameter(
        label="Symmetric",
        description="Select if the network is symmetric.",
        default_value=False,
    )
    irreflexive = knext.BoolParameter(
        label="Irreflexive",
        description="Select if the network is irreflexive.",
        default_value=False,
    )

@knext.node(
    name="Network Creation",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.network_category,
    icon_path="icons/network-2.png",
)
@knext.input_table(
    name="Input Table",
    description="Table of network varibles, necessary columns are source node, target node and tie attribute.",
)
@knext.output_port(
    name="Output Network",
    description="Network object created from the edge table.",
    port_type=network_port_type,
)
@knext.output_port_group(
    name="Output Network",
    description="Network objects created from the edge table.",
    port_type=network_port_type,
)
class NetworkFactoryNode:
    settings = NetworkSettings()

    def configure(
        self, configure_context: knext.ConfigurationContext, input_schema: knext.Schema
    ) -> NetworkPortObjectSpec:
        # Check if the parameters are set
        if not self.settings.source_label:
            raise knext.InvalidParametersError("Source column must be set.")
        if not self.settings.target_label:
            raise knext.InvalidParametersError("Target column must be set.")
        if not self.settings.weight_label:
            raise knext.InvalidParametersError("Weight column must be set.")
        if self.settings.source_label == self.settings.target_label:
            raise knext.InvalidParametersError(
                "Source and target columns must be different."
            )
        if (
            self.settings.weight_label
            and self.settings.weight_label == self.settings.source_label
        ):
            raise knext.InvalidParametersError(
                "Weight column must be different from source column."
            )
        if (
            self.settings.weight_label
            and self.settings.weight_label == self.settings.target_label
        ):
            raise knext.InvalidParametersError(
                "Weight column must be different from target column."
            )
        return NetworkPortObjectSpec(
            two_mode=self.settings.two_mode,
            symmetric=self.settings.symmetric,
            irreflexive=self.settings.irreflexive,
            source_label=self.settings.source_label,
            target_label=self.settings.target_label,
            weight_label=self.settings.weight_label,
        )

    def execute(
        self, exec_context: knext.ExecutionContext, input_table: knext.Table
    ) -> NetworkPortObject:
        settings_dict = {
            "source_label": self.settings.source_label,
            "target_label": self.settings.target_label,
            "weight_label": self.settings.weight_label,
            "two_mode": self.settings.two_mode,
            "symmetric": self.settings.symmetric,
            "irreflexive": self.settings.irreflexive,
        }
        return create_network(
            input_table.to_pandas(),
            settings_dict
        )

