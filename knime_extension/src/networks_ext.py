import knime_extension as knext

main_category = knext.category(
    path="/community",
    level_id="networks",
    name="Networks Analysis",
    description="Python Nodes for Networks Analysis",
    icon="icons/icon.png",
    locked=False,
)

import nodes.visualization.undirected_graph
import nodes.transformation.shortest_paths
