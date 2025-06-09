from util.position_algorithms import (
    DominanceStrictOptions,
    DominanceDirectionOptions,
)
import numpy as np
import pandas as pd
from util.port_objects import PositionPortObject, NetworkPortObject, NetworkPortObjectSpec

def permutation_dominance(
    pos_obj: PositionPortObject,
    strictness: DominanceStrictOptions,
    direction: DominanceDirectionOptions,
    default_value: float = None,
) -> NetworkPortObject:
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

            if direction == DominanceDirectionOptions.GREATER_THAN:
                sorted_i = np.sort(arr_i)[::-1]
                sorted_j = np.sort(arr_j)[::-1]
            else:
                sorted_i = np.sort(arr_i)
                sorted_j = np.sort(arr_j)

            if direction == DominanceDirectionOptions.GREATER_THAN:
                sorted_i, sorted_j = sorted_j, sorted_i

            weak = bool(np.all(sorted_i <= sorted_j))
            if strictness == DominanceStrictOptions.STRICT:
                dominates = weak and bool(np.any(sorted_j < sorted_i))
            else:
                dominates = weak
            if dominates:
                edges.append((node_i, node_j, 1))

    df_edges = pd.DataFrame(edges, columns=["source", "target", "dominates"])
    spec = NetworkPortObjectSpec(
        source_label="source",
        target_label="target",
        weight_label="dominates",
        symmetric=False,
        two_mode=False,
        irreflexive=True,
    )
    return NetworkPortObject(spec=spec, network=df_edges)