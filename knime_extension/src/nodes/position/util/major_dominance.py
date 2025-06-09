import numpy as np
import pandas as pd
from util.port_objects import (
    PositionPortObject,
    NetworkPortObject,
    NetworkPortObjectSpec,
)
from util.position_algorithms import (
    DominanceStrictOptions,
    DominanceDirectionOptions,
    SortingDirectionOptions,
)


def majorization_dominance(
    input: PositionPortObject,
    strictness: DominanceStrictOptions,
    dominance_direction: DominanceDirectionOptions,
    sorting_direction: SortingDirectionOptions,
    default_value: float,
) -> NetworkPortObject:
    """
    Compute a directed network of majorization dominance:
    node_j dominates node_i if the prefix sums of
    node_j's sorted position vector are all >= those of node_i,
    with at least one strict > if strictness is STRICT.
    """
    positions, dimensions = input.get_uniform_positions()
    network = []
    for node_i, vec_i in positions.items():
        for node_j, vec_j in positions.items():
            if node_i == node_j:
                continue

            pos_dict_i = vec_i
            pos_dict_j = vec_j
            arr_i = np.array([pos_dict_i.get(dim, default_value) for dim in dimensions])
            arr_j = np.array([pos_dict_j.get(dim, default_value) for dim in dimensions])

            if sorting_direction == SortingDirectionOptions.DESCENDING:
                sorted_i = np.sort(arr_i)[::-1]
                sorted_j = np.sort(arr_j)[::-1]
            else:
                sorted_i = np.sort(arr_i)
                sorted_j = np.sort(arr_j)

            prefix_i = np.cumsum(sorted_i)
            prefix_j = np.cumsum(sorted_j)

            if dominance_direction == DominanceDirectionOptions.GREATER_THAN:
                prefix_i, prefix_j = prefix_j, prefix_i
            weak = bool(np.all(prefix_i <= prefix_j))

            if strictness == DominanceStrictOptions.WEAK:
                dominates = weak
            else:
                dominates = weak and bool(np.any(prefix_i < prefix_j))
            if dominates:
                network.append((node_i, node_j, 1))
    df = pd.DataFrame(
        network, columns=["source", "target", "dominates"]
    )
    return NetworkPortObject(
        NetworkPortObjectSpec(
            source_label="source",
            target_label="target",
            weight_label="dominates",
            two_mode=False,
            symmetric=False,
            irreflexive=True,
        ),
        network=df,
    )
