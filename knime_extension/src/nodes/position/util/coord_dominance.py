import pandas as pd
from util.port_objects import NetworkPortObject, NetworkPortObjectSpec, PositionPortObject
from util.position_algorithms import DominanceStrictOptions, DominanceDirectionOptions

def coordinate_dominance(
    pos_obj: PositionPortObject,
    dominance_strict: DominanceStrictOptions,
    direction: DominanceDirectionOptions,
    default_value: float = None
) -> NetworkPortObject:
    """
    Compute the coordinate-wise (Pareto) dominance network of positions.
    Creates a directed edge (u, v) for each pair of positions u, v where
    u_i <= v_i for all dimensions i and strictly less for at least one dimension.
    The direction of comparison can be specified as either "less than" or "greater than".
    Args:
        pos_obj (PositionPortObject): The position object containing node positions.
        dominance_strict (DominanceStrictOptions): Type of dominance to compute (strict or weak).
        direction (DominanceDirectionOptions): Direction of comparison (less than or greater than).
        default_value (float, optional): Default value for missing dimensions. Defaults to None and None value in any comparison will always be true.
    """
    # Extract raw positions dict and list of dimensions
    positions, dimensions = pos_obj.get_uniform_positions()
    edges = []
    # Compare every pair of nodes
    for u, uvec in positions.items():
        for v, vvec in positions.items():
            if u == v:
                continue
            all_true = True
            strictly_less = False
            for dim in dimensions:
                uval = uvec.get(dim, default_value)
                vval = vvec.get(dim, default_value)
                if uval is None or vval is None:
                    continue
                if DominanceDirectionOptions.LESS_THAN == direction:
                    if vval < uval:
                        all_true = False
                        break
                    if uval < vval:
                        strictly_less = True
                elif DominanceDirectionOptions.GREATER_THAN == direction:
                    if vval > uval:
                        all_true = False
                        break
                    if uval > vval:
                        strictly_less = True
            if not all_true:
                continue
            if dominance_strict == DominanceStrictOptions.STRICT and not strictly_less:
                continue
            edges.append((u, v, 1))

    # Build edge DataFrame
    df_edges = pd.DataFrame(edges, columns=['source', 'target', 'dominates'])
    # Define port object spec for a directed, irreflexive network
    spec = NetworkPortObjectSpec(
        two_mode=False,
        symmetric=False,
        irreflexive=True,
        source_label='source',
        target_label='target',
        weight_label='dominates',
    )
    # Return as a NetworkPortObject
    return NetworkPortObject(spec=spec, network=df_edges)