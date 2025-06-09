import pandas as pd
import networkx as nx
from typing import List, Tuple, Any
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)

def max_flow_transform(input: NetworkPortObject) -> NetworkPortObject:
    edge_list = input.get_network()
    source_label = input.get_source_label()
    target_label = input.get_target_label()
    weight_label = input.get_weight_label()
    two_mode = input.is_two_mode()
    symmetric = input.is_symmetric()
    irreflexive = input.is_irreflexive()

    G = nx.from_pandas_edgelist(
        edge_list,
        source=source_label,
        target=target_label,
        edge_attr=weight_label,
        create_using=nx.DiGraph() if not symmetric else nx.Graph(),
    )

    if two_mode:
        mode_u = list(edge_list[source_label].unique())
        mode_v = list(edge_list[target_label].unique())
    else:
        mode_u = list(G.nodes())
        mode_v = mode_u

    results: List[Tuple[Any, Any, float]] = []

    if symmetric:
        T = nx.gomory_hu_tree(G, capacity="capacity")
        def min_cut(u, v):
            path = nx.shortest_path(T, u, v)
            return min(T[a][b]["weight"] for a, b in zip(path, path[1:]))

        for u in mode_u:
            for v in mode_v:
                if irreflexive and u == v:
                    continue
                if two_mode and (u not in mode_u or v not in mode_v):
                    continue
                flow = min_cut(u, v) if (u in T and v in T) else 0.0
                results.append((u, v, flow))

    else:
        for u in mode_u:
            for v in mode_v:
                if irreflexive and u == v:
                    continue
                if two_mode and (u not in mode_u or v not in mode_v):
                    continue
                try:
                    flow_value, _ = nx.maximum_flow(
                        G, u, v, capacity="capacity", flow_func=nx.preflow_push
                    )
                except (nx.NetworkXError, nx.NetworkXNoPath):
                    flow_value = 0.0
                results.append((u, v, flow_value))

    df = pd.DataFrame(results, columns=[source_label, target_label, "max_flow"])
    return NetworkPortObject(
        NetworkPortObjectSpec(
            source_label=source_label,
            target_label=target_label,
            weight_label="max_flow",
            irreflexive=irreflexive,
            symmetric=symmetric,
            two_mode=two_mode,
        ),
        df,
    )