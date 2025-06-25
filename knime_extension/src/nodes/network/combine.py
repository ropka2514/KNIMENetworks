import knime.extension as knext

import networks_ext

# import util.network_algorithms as algo
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)
from util.port_types import (
    network_port_type,
)
import pandas as pd


class MethodOptions(knext.EnumParameterOptions):

    UNION = ("Union", "Combine all nodes and edges from both networks.")
    INTERSECTION = (
        "Intersection",
        "Combine only nodes and edges that are present in both networks.",
    )


class ValueOptions(knext.EnumParameterOptions):
    """
    Options for combining values.
    """

    PRIORITY = (
        "Priority",
        "Use the value from the first network if available, otherwise from the second, and so on.",
    )
    MIN = ("Min", "Take the minimum value from all networks.")
    MAX = ("Max", "Take the maximum value from all networks.")
    AVERAGE = ("Average", "Take the average value from all networks.")
    BINARY = (
        "Binary",
        "Combine values using a binary operation.  Existing values will be replaced with 1 for existence of the attribute, otherwise 0.",
    )


@knext.parameter_group(label="Combine Settings")
class CombineSettings:
    method = knext.EnumParameter(
        label="Combine Method",
        description="Method to combine networks.",
        enum=MethodOptions,
        default_value=MethodOptions.UNION.name,
    )
    value = knext.EnumParameter(
        label="Value Method",
        description="Method to determine the edge values in the resulting network.",
        enum=ValueOptions,
        default_value=ValueOptions.PRIORITY.name,
    )


@knext.node(
    name="Network Merge",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_port_group(
    name="Input Networks",
    description="Networks to combine.",
    port_type=network_port_type,
)
@knext.output_port(
    name="Output Network",
    description="Combined network.",
    port_type=network_port_type,
)
class CombineNetworksNode:
    """
    Node to combine multiple networks into one.
    """

    settings = CombineSettings()

    def configure(
        self, configure_context: knext.ConfigurationContext, inputs_schema: list[NetworkPortObject]
    ) -> NetworkPortObject:
        """
        Configure the node based on the provided settings.
        """
        # Validate settings if needed
        return NetworkPortObjectSpec(
            source_label='source',
            target_label='target',
            weight_label='value',
            irreflexive=True,
            symmetric=False,
            two_mode=False,
        )

    def execute(self, input_networks: list[NetworkPortObject]) -> NetworkPortObject:
        """
        Combine the input networks based on the selected method and value handling.
        """
        if not input_networks:
            raise knext.ExecutionError("No input networks provided.")
        if len(input_networks) == 1:
            return input_networks[0]
        
        for net in input_networks:
            # if network symmetric, add all reverse edges and their values to dataframe edgelist
            if net.is_symmetric():
                reverse_edges = net._network.copy()
                reverse_edges[net.get_source_label()] = net._network[net.get_target_label()]
                reverse_edges[net.get_target_label()] = net._network[net.get_source_label()]
                net._network = pd.concat([net._network, reverse_edges], ignore_index=True)

        edge_sets = [
            set(
                zip(
                    net._network[net.get_source_label()],
                    net._network[net.get_target_label()],
                )
            )
            for net in input_networks
        ]

        if self.settings.method == MethodOptions.UNION.name:
            combined_edges = set().union(*edge_sets)
        else:
            combined_edges = set(edge_sets[0]).intersection(*edge_sets)

        combined_rows = []
        for u, v in combined_edges:
            vals = []
            for net in input_networks:
                mask = (net._network[net.get_source_label()] == u) & (
                    net._network[net.get_target_label()] == v
                )
                if mask.any():
                    vals.append(net._network.loc[mask, net.get_weight_label()].iloc[0])
                else:
                    vals.append(None)

            method = self.settings.value
            if method == ValueOptions.PRIORITY.name:
                combined_val = next((x for x in vals if x is not None), None)
            elif method == ValueOptions.MIN.name:
                nums = [x for x in vals if x is not None]
                combined_val = min(nums) if nums else None
            elif method == ValueOptions.MAX.name:
                nums = [x for x in vals if x is not None]
                combined_val = max(nums) if nums else None
            elif method == ValueOptions.AVERAGE.name:
                nums = [x for x in vals if isinstance(x, (int, float))]
                combined_val = sum(nums) / len(nums) if nums else None
            elif method == ValueOptions.BINARY.name:
                combined_val = 1 if any(x is not None for x in vals) else 0
            else:
                combined_val = None

            combined_rows.append({"source": u, "target": v, "value": combined_val})

        # Build the result DataFrame
        result_df = pd.DataFrame(combined_rows)

        # Wrap in a NetworkPortObject and return
        spec = NetworkPortObjectSpec(
            source_label="source",
            target_label="target",
            weight_label="value",
            irreflexive=True,
            symmetric=False,
            two_mode=False,
        )
        return NetworkPortObject(
            network=result_df,
            spec=spec,
        )
