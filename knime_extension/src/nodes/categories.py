import knime_extension as knext

main_category = knext.category(
    path="/community",
    level_id="network_analysis",
    name="Network Analysis",
    description="Nodes for Positional Network Analysis",
    icon="icons/icon.png",
    locked=False,
)
network_category = knext.category(
    path="/community/network_analysis",
    level_id="network",
    name="Network Nodes",
    description="Nodes forh handling network data",
    icon="icons/icon.png",
    locked=False,
)
position_category = knext.category(
    path="/community/network_analysis",
    level_id="position",
    name="Position Nodes",
    description="Nodes for handling positional data",
    icon="icons/icon.png",
    locked=False,
)
attribute_category = knext.category(
    path="/community/network_analysis",
    level_id="attribute",
    name="Attribute Nodes",
    description="Nodes for handling attribute data",
    icon="icons/icon.png",
    locked=False,
)
