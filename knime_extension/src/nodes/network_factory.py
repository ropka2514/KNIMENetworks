import knime.extension as knext
import networkx as nx
import pandas as pd

import networks_ext
from util.port_types import (
    NetworkPortObject,
    NetworkPortObjectSpec,
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
    undirected = knext.BoolParameter(
        label="Symmetric",
        description="Select if the network is undirected.",
        default_value=False,
    )


@knext.node(
    name="Network Factory",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/icon-missing.png",
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
class NetworkFactoryNode:
    settings = NetworkSettings()
    # format_graph = knext.BoolParameter(
    #     label="Pickle the output of the node",
    #     description="Select if the output should be pickled.",
    #     default_value=False,
    # )

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
        # for col in input_schema._columns:
        #     if col.name == self.weight_label:
        #         weight_column = col
        return NetworkPortObjectSpec(
            two_mode=self.settings.two_mode,
            undirected=self.settings.undirected,
            # format_graph=self.format_graph,
            source_label=self.settings.source_label,
            target_label=self.settings.target_label,
            weight_label=self.settings.weight_label,
            # weight_column=knext.Column(col.ktype, col.name),
        )

    def execute(
        self, exec_context: knext.ExecutionContext, input_table: knext.Table
    ) -> NetworkPortObject:
        df = input_table.to_pandas()

        source_label = self.settings.source_label
        target_label = self.settings.target_label
        weight_label = self.settings.weight_label
        two_mode = self.settings.two_mode
        undirected = self.settings.undirected
        format_graph = False  # self.format_graph

        if format_graph:
            if two_mode:
                G = nx.DiGraph() if undirected else nx.Graph()
                for _, row in df.iterrows():
                    source_val = row[source_label]
                    target_val = row[target_label]
                    G.add_node(source_val, bipartite=0)
                    G.add_node(target_val, bipartite=1)
                    if weight_label:
                        G.add_edge(source_val, target_val, weight=row[weight_label])
                    else:
                        G.add_edge(source_val, target_val)
            else:
                G = nx.from_pandas_edgelist(
                    df,
                    source=source_label,
                    target=target_label,
                    edge_attr=weight_label,
                    create_using=nx.Graph() if not undirected else nx.DiGraph(),
                )
            network_obj = NetworkPortObject(self.spec, G)
        else:
            if weight_label is None:
                df[weight_label] = 1
            edge_df = df[[source_label, target_label, weight_label]]

            network_table = knext.Table.from_pandas(edge_df)

            network_obj = NetworkPortObject(
                NetworkPortObjectSpec(
                    two_mode=two_mode,
                    undirected=undirected,
                    # format_graph=format_graph,
                    source_label=source_label,
                    target_label=target_label,
                    weight_label=weight_label,
                    # weight_column=knext.Column(knext.String(), weight_label),
                ),
                network_table,
            )

        return network_obj
