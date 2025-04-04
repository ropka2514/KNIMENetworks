import knime_extension as knext

# from nodes.categories import main_category

main_category = knext.category(
    path="/community",
    level_id="networks",
    name="Positional Network Analysis",
    description="Python Nodes for Networks Analysis",
    icon="icons/icon.png",
    locked=False,
)

import nodes.network_factory
import nodes.network_transformation
import nodes.network_table
import nodes.position_factory
import nodes.position_dominance