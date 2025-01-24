import knime.extension as knext
import networkx as nx
import pandas as pd
from ..categories import transform_category

@knext.node(
    name="Shortest Paths",
    node_type=knext.NodeType.MANIPULATOR,
    category=transform_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_table(
    name="Network Data",
    description="Data table containing the network data as an edge table [source node, target node, weight].",
)
@knext.output_table(
    name="Shortest Paths Network",
    description="Data table containing the shortest paths between all pairs of nodes.",
)
class ShortestPathsNode:
    def configure(self, configure_context: knext.ConfigurationContext, input_schema: knext.Schema):
        return input_schema
    
    def execute(self, exec_context: knext.ExecutionContext, input_table: knext.Table):
        df = input_table.to_pandas()

        G = nx.Graph()
        edges = zip(
            df[df.columns[0]],
            df[df.columns[1]],
            df[df.columns[2]] if len(df.columns) > 2 else [1] * len(df),
        )

        G.add_weighted_edges_from(edges)
        shortest_paths = nx.all_pairs_bellman_ford_path_length(G, weight="weight")

        data = []
        for source, targets in shortest_paths:
            for target, weight in targets.items():
                data.append([source, target, weight])

        output_table = knext.Table.from_pandas(pd.DataFrame(data, columns=["source", "target", "weight"]))
        return output_table
    