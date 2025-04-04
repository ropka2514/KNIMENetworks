import knime.extension as knext
import pandas as pd
import networkx as nx

import networks_ext
from util.port_types import (
    NetworkPortObject,
    NetworkPortObjectSpec,
    network_port_type,
)


@knext.node(
    name="Node Positions",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_port_group(
    name="Input Network",
    description="Input network to compute positions.",
    port_type=network_port_type,
)
@knext.output_table(
    name="Output Table",
    description="Output table with network positions.",
)
class NetworkPositionNode:
    #  TODO: add neutral value for nonexistent edges, redo the design, pos = [(tie value) for existing edges ... (attr) for node attributes] ]

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema: NetworkPortObjectSpec,
    ) -> knext.Schema:
        # ktype1 = knext.string()
        # ktype2 = input_schema.weight_column.ktype
        # return knext.Schema([ktype1,ktype1, ktype2],[input_schema.source_label, input_schema.target_label, input_schema.weight_label])
        return None
    def execute(self, context, input_networks: list[NetworkPortObject]) -> knext.Table:
        input_network = input_networks[0]
        df = input_network.get_network().to_pandas()
        if input_network.is_two_mode():
            # target_nodes = pd.Series(df[input_network.get_target_label()].tolist()).unique()
            # source_nodes = pd.Series(df[input_network.get_source_label()].tolist()).unique()
            pos = df.pivot_table(index=input_network.get_source_label(), columns=input_network.get_target_label(), values=input_network.get_weight_label(), fill_value=0)
        else:
            # target_nodes = pd.Series(df[input_network.get_source_label()].tolist() + df[input_network.get_target_label()].tolist()).unique()
            # source_nodes = pd.Series(df[input_network.get_target_label()].tolist() + df[input_network.get_source_label()].tolist()).unique()
            pos = df.pivot_table(index=input_network.get_source_label(), columns=input_network.get_target_label(), values=input_network.get_weight_label(), fill_value=0)
            pos = pos.add(pos.T, fill_value=0) 
            # sort the columns
            # pos = pos.reindex(sorted(pos.columns), axis=1)
            # set all missing values to 0
        pos = pos.fillna(0)
        pos = pos.loc[pos.index, pos.index]
        

        return knext.Table.from_pandas(pos)


