from util.port_objects import (    PositionPortObject,
    NetworkPortObject,
    NetworkPortObjectSpec,
)
from util.position_algorithms import (
    DominanceStrictOptions,
    DominanceDirectionOptions,
)
import numpy as np
import pandas as pd

def neighborhood_dominance(
    pos_obj: PositionPortObject,
    strictness: DominanceStrictOptions,
    direction: DominanceDirectionOptions,
    default_value: float = None,
) -> NetworkPortObject:
    """
    Compute neighborhood dominance:
    Node j dominates i if, after optional inversion and sorting,
    at the first differing coordinate j's value is >= (weak) or > (strict) that of i.
    """
    positions = pos_obj.positions
    dimensions = pos_obj.dimensions
    edges = []
    for node_i, pos_i in positions.items():
        for node_j, pos_j in positions.items():
            if node_i == node_j:
                continue
            vec_i = [pos_i.get(dim, default_value) for dim in dimensions]
            vec_j = [pos_j.get(dim, default_value) for dim in dimensions]
            arr_i = np.array(vec_i)
            arr_j = np.array(vec_j)
            if direction == DominanceDirectionOptions.LESS_THAN:
                arr_i = -arr_i
                arr_j = -arr_j
            weak = bool(np.all(arr_i <= arr_j))
            if strictness == DominanceStrictOptions.STRICT:
                strict = bool(np.any(arr_i < arr_j))
                dominates = weak and strict
            else:
                dominates = weak
            if dominates:
                edges.append((node_i, node_j))

    df = pd.DataFrame(edges, columns=["source", "target", "dominates"])
    spec = NetworkPortObjectSpec(
        source_label="source",
        target_label="target",
        weight_label="dominates",
        symmetric=False,
        two_mode=False,
        irreflexive=True,
    )
    return NetworkPortObject(spec=spec, network=df)