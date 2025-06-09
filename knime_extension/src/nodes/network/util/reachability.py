import pandas as pd
import networkx as nx
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)

def reachability_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Computes the reachability transform of a network. Doesn't take esge values into account.
    It computes the transitive closure of the network.
    The output is a NetworkPortObject with the reachability network.
    """
    source_label = networkObj.get_source_label()
    target_label = networkObj.get_target_label()

    if networkObj.is_two_mode():
        raise ValueError(
            "Reachability transform is not supported for two-mode networks."
        )

    df = networkObj.get_network()
    G = nx.from_pandas_edgelist(
        df,
        source=source_label,
        target=target_label,
        create_using=nx.DiGraph() if not networkObj.is_symmetric() else nx.Graph(),
    )
    G_transitive = nx.transitive_closure(
        G, reflexive=True if networkObj.is_irreflexive() else None
    )
    df = nx.to_pandas_edgelist(G_transitive, source=source_label, target=target_label)
    df["reachable"] = 1

    return NetworkPortObject(
        NetworkPortObjectSpec(
            source_label=source_label,
            target_label=target_label,
            weight_label="reachable",
            irreflexive=networkObj.is_irreflexive(),
            symmetric=networkObj.is_symmetric(),
            two_mode=networkObj.is_two_mode(),
        ),
        df,
    )

def k_reachability_transform(
    networkObj: NetworkPortObject, max_step: int
) -> NetworkPortObject:
    """
    Computes the k-reachability transform of a network.
    The output is a NetworkPortObject with the k-step reachability of nodes.
    """
    source_label = networkObj.get_source_label()
    target_label = networkObj.get_target_label()

    if networkObj.is_two_mode():
        raise ValueError(
            "k-reachability transform is not supported for two-mode networks."
        )

    df = networkObj.get_network()
    G = nx.from_pandas_edgelist(
        df,
        source=source_label,
        target=target_label,
        create_using=nx.DiGraph() if not networkObj.is_symmetric() else nx.Graph(),
    )
    reachability = {node: {} for node in G.nodes}
    node_queue = {node: set(G.neighbors(node)) for node in G.nodes}
    for step in range(1, max_step + 1):
        for source in G.nodes:
            next_queue = set()
            for target in node_queue[source]:
                if target in reachability[source]:
                    continue
                reachability[source][target] = step
                if max_step < (2 * step):
                    remaining_steps = max_step - step
                    valid_extensions = {
                        k: v
                        for k, v in reachability[target].items()
                        if v <= remaining_steps
                    }
                    new_targets = set(valid_extensions.keys()) - set(
                        reachability[source].keys()
                    )
                    new_reachability = {
                        k: v + step
                        for k, v in valid_extensions.items()
                        if k in new_targets
                    }
                    reachability.update(new_reachability)
                else:
                    next_queue.update(G.neighbors(target))
            node_queue[source] = next_queue

    edge_list = [
        (source, target, 1)
        for source, targets in reachability.items()
        for target in targets.keys()
    ]

    return NetworkPortObject(
        NetworkPortObjectSpec(
            source_label=source_label,
            target_label=target_label,
            weight_label="reachable",
            irreflexive=networkObj.is_irreflexive(),
            symmetric=networkObj.is_symmetric(),
            two_mode=networkObj.is_two_mode(),
        ),
        pd.DataFrame(edge_list, columns=[source_label, target_label, "reachable"])
    )