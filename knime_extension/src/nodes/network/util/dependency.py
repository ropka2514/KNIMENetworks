import pandas as pd
import networkx as nx
from networkx.algorithms.centrality.betweenness import (
    _single_source_shortest_path_basic,
    _single_source_dijkstra_path_basic,
)
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)

def dependency_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Compute δ_s(v) for all ordered pairs (s,v) in a NetworkX graph G.
    Returns a new complete network where an edge (v,s) = δ_s(v).
    If weight is None, unweighted shortest paths are used; otherwise, weighted.
    """
    source_label = networkObj.get_source_label()
    target_label = networkObj.get_target_label()
    weight_label = networkObj.get_weight_label()

    if networkObj.is_two_mode():
        raise ValueError(
            "Dependency transform is not supported for two-mode networks. Consider projection to one-mode network."
        )
    df = networkObj.get_network()
    if not pd.api.types.is_numeric_dtype(df[weight_label]):
        raise ValueError(
            "Weight column must be numeric. Consider using adjacency transformation first."
        )
    if (df[weight_label] <= 0).any():
        raise ValueError(
            "Weight column must be positive. Consider using another network transformation first."
        )

    G = nx.from_pandas_edgelist(
        df,
        source=source_label,
        target=target_label,
        edge_attr=weight_label,
        create_using=nx.Graph() if networkObj.is_symmetric() else nx.DiGraph(),
    )

    nodes = list(G.nodes())
    newGraph = nx.DiGraph()

    for s in nodes:
        # Use NetworkX's internal shortest-path routine to get S, P, sigma
        if weight_label is None:
            S, P, sigma, _ = _single_source_shortest_path_basic(G, s)
        else:
            S, P, sigma, _ = _single_source_dijkstra_path_basic(G, s, weight_label)

        # Back-propagate to compute δ_s(v)
        delta = {v: 0.0 for v in nodes}
        while S:
            w = S.pop()
            for u in P[w]:
                delta[u] += (sigma[u] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                newGraph.add_edge(s, w, dependency=delta[w])

    df = nx.to_pandas_edgelist(newGraph, source=source_label, target=target_label)

    return NetworkPortObject(
        NetworkPortObjectSpec(
            source_label=source_label,
            target_label=target_label,
            weight_label="dependency",
            irreflexive=networkObj.is_irreflexive(),
            symmetric=False, 
            two_mode=networkObj.is_two_mode(),
        ),
        df,
    )
