import numpy as np
import pandas as pd
from util.position_algorithms import (
    DominanceStrictOptions,
    DominanceDirectionOptions,
    SortingDirectionOptions,
)
from util.port_objects import (
    PositionPortObject,
    NetworkPortObject,
    NetworkPortObjectSpec,
)


def lexicographic_dominance(
    pos_obj: PositionPortObject,
    strictness: DominanceStrictOptions,
    direction: DominanceDirectionOptions,
    sorting_direction: SortingDirectionOptions | None,
    default_value: float = None,
) -> NetworkPortObject:
    """
    Compute lexicographic dominance:
    Node j dominates i if, after optional inversion and sorting,
    at the first differing coordinate j's value is >= (weak) or > (strict) that of i.
    """
    # Extract raw positions dict and list of dimensions
    positions, dimensions = pos_obj.get_uniform_positions()

    edges = []
    for node_i, pos_i in positions.items():
        for node_j, pos_j in positions.items():
            if node_i == node_j:
                continue
            vec_i = [pos_i.get(dim, default_value) for dim in dimensions]
            vec_j = [pos_j.get(dim, default_value) for dim in dimensions]
            arr_i = np.array(vec_i)
            arr_j = np.array(vec_j)

            # sort according to sorting_direction
            if sorting_direction == SortingDirectionOptions.DESCENDING:
                sorted_i = np.sort(arr_i)[::-1]
                sorted_j = np.sort(arr_j)[::-1]
            elif sorting_direction == SortingDirectionOptions.ASCENDING:
                sorted_i = np.sort(arr_i)
                sorted_j = np.sort(arr_j)
            else:
                sorted_i = arr_i
                sorted_j = arr_j

            # find first difference
            diffs = sorted_i != sorted_j
            if not np.any(diffs):
                continue
            k = np.argmax(diffs)

            if direction == DominanceDirectionOptions.GREATER_THAN:
                # invert comparison for greater than direction
                sorted_i, sorted_j = sorted_j, sorted_i

            if strictness == DominanceStrictOptions.WEAK:
                edges.append(
                    (node_i, node_j, 1)
                    if sorted_j[k] >= sorted_i[k]
                    else (node_j, node_i, 1)
                )
            else:
                edges.append(
                    (node_i, node_j, 1)
                    if sorted_j[k] > sorted_i[k]
                    else (node_j, node_i, 1)
                )
    # build edge list DataFrame
    df_edges = pd.DataFrame(edges, columns=["source", "target", "dominates"])
    spec = NetworkPortObjectSpec(
        source_label="source",
        target_label="target",
        weight_label="dominates",
        symmetric=False,
        two_mode=False,
    )
    return NetworkPortObject(spec=spec, network=df_edges)
