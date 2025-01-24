import knime_extension as knext

visual_category = knext.category(
    path="/community/networks",
    level_id="visual",
    name="Visualizations",
    description="Python Nodes for Networks Visualization",
    icon="icons/icon-missing.png",
    locked=False,
)

transform_category = knext.category(
    path="/community/networks",
    level_id="transform",
    name="Transformations",
    description="Python Nodes for Networks Transformations",
    icon="icons/icon-missing.png",
    locked=False,
)