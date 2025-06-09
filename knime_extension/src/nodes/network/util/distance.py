import pandas as pd
import networkx as nx

from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)



def distance_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Computes the distance transform of a network.
    The output is a NetworkPortObject with the distances between all nodes.
    """
    source_label = networkObj.get_source_label()
    target_label = networkObj.get_target_label()
    weight_label = networkObj.get_weight_label()

    if networkObj.is_two_mode():
        raise ValueError(
            "Distance transform is not supported for two-mode networks. Consider projection to one-mode network."
        )
    df = networkObj.get_network()
    if not pd.api.types.is_numeric_dtype(df[weight_label]):
        raise ValueError("Weight column must be numeric.")
    if (df[weight_label] <= 0).any():
        raise ValueError("Weight column must be positive.")

    G = nx.from_pandas_edgelist(
        df,
        source=source_label,
        target=target_label,
        edge_attr=weight_label,
        create_using=nx.Graph() if networkObj.is_symmetric() else nx.DiGraph(),
    )

    all_pairs_distances = dict(
        nx.all_pairs_dijkstra_path_length(G, weight=weight_label)
    )
    edges = [
        (source, target, distance)
        for source, targets in all_pairs_distances.items()
        for target, distance in targets.items()
        if source != target
    ]
    df = pd.DataFrame(edges, columns=[source_label, target_label, "distance"])
    if networkObj.is_symmetric():
        df_sorted = df.apply(
            lambda row: sorted([row[source_label], row[target_label]])
            + [row["distance"]],
            axis=1,
            result_type="expand",
        )
        df_sorted.columns = [source_label, target_label, "distance"]
        df_sorted = df_sorted.drop_duplicates()
        df = df_sorted

    return NetworkPortObject(
        NetworkPortObjectSpec(
            source_label=source_label,
            target_label=target_label,
            weight_label="distance",
            symmetric=networkObj.is_symmetric(),
            two_mode=networkObj.is_two_mode(),
        ),
        df,
    )