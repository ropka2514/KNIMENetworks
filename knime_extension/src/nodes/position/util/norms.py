import math
from util.port_objects import (
    PositionPortObject,
    PositionPortObjectSpec,
)

def euclidean_norm_transform(
    input: PositionPortObject, default_value=None
) -> PositionPortObject:
    """
    Compute the Euclidean (L₂) norm for each node’s position vector.
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['euclidean'] = float
    """
    positions, _ = input.get_uniform_positions()
    new_positions = {}
    for node_id, coord_map in positions.items():
        if default_value is not None:
            squared_sum = sum(
                (coord_map.get(dim, default_value) ** 2)
                for dim in input.get_dimensions()
            )
        else:
            squared_sum = sum(value**2 for value in coord_map.values())
        new_positions[node_id] = {"euclidean": math.sqrt(squared_sum)}

    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=[(new_positions, ["euclidean"], "euclidean")],
    )


def manhattan_norm_transform(
    input: PositionPortObject, default_value=None
) -> PositionPortObject:
    """
    Compute the Manhattan (L₁) norm for each node’s position vector.
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['manhattan'] = float
    """
    positions, all_dims = input.get_uniform_positions()
    new_positions = {}
    for node_id, coord_map in positions.items():
        if default_value is not None:
            new_positions[node_id] = {
                "manhattan": sum(
                    abs(coord_map.get(dim, default_value)) for dim in all_dims
                )
            }
        else:
            new_positions[node_id] = {
                "manhattan": sum(abs(value) for value in coord_map.values())
            }
    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=[(new_positions, ["manhattan"], "manhattan")],
    )

def average_transform(
    input: PositionPortObject, default_value=None
) -> PositionPortObject:
    """
    Compute the average of all coordinates for each node’s position vector.
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['average'] = float
    """
    positions, all_dims = input.get_uniform_positions()
    new_positions = {}
    for node_id, coord_map in positions.items():
        if default_value is not None:
            total = sum(coord_map.get(dim, default_value) for dim in all_dims)
            count = len(all_dims)
        else:
            if coord_map:
                total = sum(coord_map.values())
                count = len(coord_map)
                new_positions[node_id] = {"average": total / count}
            else:
                new_positions[node_id] = {"average": 0.0}
    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=[(new_positions, ["average"], "average")],
    )


def sum_transform(input: PositionPortObject, default_value=None) -> PositionPortObject:
    """
    Compute the sum of all coordinates for each node’s position vector.
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['sum'] = float
    """
    positions, _ = input.get_uniform_positions()
    new_positions = {}
    for node_id, coord_map in positions.items():
        if default_value is not None:
            sum_value = sum(
                coord_map.get(dim, default_value) for dim in input.get_dimensions()
            )
        else:
            sum_value = sum(coord_map.values())
        new_positions[node_id] = {"sum": sum_value}
    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=[(new_positions,["sum"], "sum")],
    )