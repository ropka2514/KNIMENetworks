import math
import statistics
from util.port_objects import (
    PositionPortObject,
    PositionPortObjectSpec,
)



def inverse_transform(
    input: PositionPortObject, default_value=None, epsilon: float = 1e-6
) -> PositionPortObject:
    """
    Compute the inverses of each coordinate (1 / (p_i + epsilon)).
    Input:
        positions: dict[node_id][dim_name] = float
        epsilon: small constant to avoid division by zero
    Returns:
        new_positions: dict[node_id][dim_name] = float
    """
    positions, all_dims = input.get_uniform_positions()

    for node_id, coord_map in positions.items():
        if default_value is not None:
            for dim in all_dims:
                value = coord_map.get(dim, default_value)
                positions[node_id][dim] = 1.0 / (value + epsilon)
        else:
            for value in coord_map.values():
                positions[node_id][dim] = 1.0 / (value + epsilon)

    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=positions,
        dimensions=all_dims,
    )


def log_transform(input: PositionPortObject, default_value=None) -> PositionPortObject:
    """
    Compute the sum of log-transformed coordinates: sum(log(p_i + 1)).
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['log_sum'] = float
    """
    positions, all_dims = input.get_uniform_positions()

    for node_id, coord_map in positions.items():
        if default_value is not None:
            for dim in all_dims:
                value = coord_map.get(dim, default_value)
                positions[node_id][dim] = math.log(value + 1.0)
        else:
            for dim, value in coord_map.items():
                positions[node_id][dim] = math.log(value + 1.0)

    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=positions,
        dimensions=all_dims,
    )


def zscore_transform(
    input: PositionPortObject, default_value=None
) -> PositionPortObject:
    """
    Standardize each dimension (z-score) across all nodes, then compute the
    Euclidean norm of the resulting standardized vector for each node.
    Input:
        positions: dict[node_id][dim_name] = float
    Returns:
        new_positions: dict[node_id]['zscore_norm'] = float
    """
    positions, all_dims = input.get_uniform_positions()

    dim_values = {dim: [] for dim in all_dims}
    for node_id, coord_map in positions.items():
        if default_value is not None:
            for dim in all_dims:
                val = coord_map.get(dim, default_value)
                dim_values[dim].append(val)
        else:
            for dim, val in coord_map.items():
                if not isinstance(val, (int, float)):
                    raise ValueError(
                        f"Invalid value '{val}' for dimension '{dim}' in node '{node_id}'. Expected numeric type."
                    )
                dim_values[dim].append(val)

    dim_stats = {}
    for dim in all_dims:
        vals = dim_values[dim]
        mean = statistics.mean(vals)
        stdev = statistics.pstdev(vals)
        dim_stats[dim] = (mean, stdev)

    if default_value is not None:
        for node_id, coord_map in positions.items():
            for dim in all_dims:
                raw_val = coord_map.get(dim, default_value)
                mean, stdev = dim_stats[dim]
                if stdev > 0:
                    z = (raw_val - mean) / stdev
                else:
                    z = 0.0
                positions[node_id][dim] = z
    else:
        for node_id, coord_map in positions.items():
            for dim, val in coord_map.items():
                if not isinstance(val, (int, float)):
                    raise ValueError(
                        f"Invalid value '{val}' for dimension '{dim}' in node '{node_id}'. Expected numeric type."
                    )
                mean, stdev = dim_stats[dim]
                if stdev > 0:
                    z = (val - mean) / stdev
                else:
                    z = 0.0
                positions[node_id][dim] = z

    return PositionPortObject(
        spec=PositionPortObjectSpec(
            node_column=input.spec.node_column,
        ),
        positions=positions,
        dimensions=all_dims,
    )