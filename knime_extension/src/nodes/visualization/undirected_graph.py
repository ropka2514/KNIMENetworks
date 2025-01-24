import knime_extension as knext
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

from ..categories import visual_category

@knext.node(
    id="undirected_network_visualization",
    name="Undirected Network Visualization",
    node_type=knext.NodeType.VISUALIZER,
    category=visual_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_table(
    name="Network Data",
    description="Data table containing the network data as an edge table [source node, target node, weight].",
)
@knext.output_view(
    name="Output Table",
    description="Displays the network graph based on the edge table.",
)
class UndirectedNetworkVisualizationNode:
    def execute(self, exec_context: knext.ExecutionContext, input_table: knext.Table):
        df = input_table.to_pandas()

        G = nx.Graph()
        edges = zip(
            df[df.columns[0]],
            df[df.columns[1]],
            df[df.columns[2]] if len(df.columns) > 2 else [1] * len(df),
        )
        G.add_weighted_edges_from(edges)

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="skyblue",
            edge_color="gray",
            font_size=10,
            node_size=500,
            width=1.5,
        )
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        return knext.view_png(buf.getvalue())

        # img_base64 = base64.b64encode(buf.getvalue()).decode()
        html_table = df.head().to_html(index=False)  # Convert DataFrame to HTML table
        html_output = f"""
        <html>
            <body>
                <img src="data:image/png;base64,{img_base64}" alt="Graph Visualization">
                <p>Below is the head of the input table:</p>
                {html_table}
            </body>
        </html>
        """
        
        return knext.view_html(html_output)
    
    def configure(self, configure_context: knext.ConfigurationContext, input_schema: knext.Schema):
        # The output schema is the same as the input schema for this test node
        return None