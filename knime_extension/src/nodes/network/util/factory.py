import pandas as pd
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)


#+-----------------------------------------------------------+
#| Network Factory                                           |
#+-----------------------------------------------------------+

def create_network(table: pd.DataFrame, settings: dict) -> NetworkPortObject:
    """
    Creates a network from a KNIME table.
    """
    df = table

    source_label = settings["source_label"]
    target_label = settings["target_label"]
    weight_label = settings["weight_label"]
    two_mode = settings["two_mode"]
    symmetric = settings["symmetric"]
    irreflexive = settings["irreflexive"]

    if weight_label is None:
        df[weight_label] = 1
    edge_df = df[[source_label, target_label, weight_label]]
    network_table = edge_df
    network_obj = NetworkPortObject(
        NetworkPortObjectSpec(
            two_mode=two_mode,
            symmetric=symmetric,
            irreflexive=irreflexive,
            source_label=source_label,
            target_label=target_label,
            weight_label=weight_label,
        ),
        network_table,
    )

    return network_obj

