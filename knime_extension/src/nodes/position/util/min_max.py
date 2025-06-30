from util.port_objects import (
    PositionPortObject,
    PositionPortObjectSpec,
)

def max_transform(input: PositionPortObject, default_value=None) -> PositionPortObject:
    """
    Compute the maximum coordinate (L_∞) for each node’s position vector.
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['max_coordinate'] = float
    """
    positions, all_dims = input.get_uniform_positions()
    new_positions = {}
    for node_id, coord_map in positions.items():
        if default_value is not None:
            new_positions[node_id] = {
                "max_coordinate": max(
                    coord_map.get(dim, default_value) for dim in all_dims
                )
            }
        else:
            if coord_map:
                new_positions[node_id] = {
                    "max_coordinate": max(abs(value) for value in coord_map.values())
                }
            else:
                new_positions[node_id] = {"max_coordinate": None}
    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=new_positions,
        dimensions=["max"],
    )


def min_transform(input: PositionPortObject, default_value=None) -> PositionPortObject:
    """
    Compute the minimum coordinate for each node’s position vector.
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['min_coordinate'] = float
    """
    positions, all_dims = input.get_uniform_positions()
    new_positions = {}
    for node_id, coord_map in positions.items():
        if default_value is not None:
            min_value = min(coord_map.get(dim, default_value) for dim in all_dims)
        else:
            if coord_map:
                min_value = min(coord_map.values())
            else:
                min_value = None
        new_positions[node_id] = {"min_coordinate": min_value}
    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=new_positions,
        dimensions=["min"],
    )
