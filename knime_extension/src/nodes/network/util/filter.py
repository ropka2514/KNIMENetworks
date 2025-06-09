import pandas as pd
import numpy as np
from util.port_objects import NetworkPortObject

# Filtering transformation function
def filter_transform(
    networkObj: NetworkPortObject,
    degree_type: str,
    filter_type: str,
    filter_threshold: str,
    filter_mode: str,
    filter_value: float,
    strength_mode: bool
) -> NetworkPortObject:
    """
    Filter nodes or edges based on user settings:
    - degree_type: "OUT", "IN", or "TOTAL" for node strength calculation
    - filter_type: "NODE" or "EDGE"
    - filter_threshold: "ABSOLUTE_THRESHOLD" or "PERCENTILE_THRESHOLD"
    - filter_mode: "GREATER" or "LESS"
    - filter_value: threshold value or percentile
    - strength_mode: if True and filter_type=="NODE", filter on node strength; otherwise filter on degree
    """
    src = networkObj.get_source_label()
    tgt = networkObj.get_target_label()
    wgt = networkObj.get_weight_label()
    df = networkObj.get_network().copy()

    if filter_type == "NODE":
        # Compute node metric: strength or degree based on degree_type
        if strength_mode:
            if degree_type == "OUT":
                node_vals = df.groupby(src)[wgt].sum()
            elif degree_type == "IN":
                node_vals = df.groupby(tgt)[wgt].sum()
            elif degree_type == "TOTAL":
                node_vals = pd.concat([
                    df.groupby(src)[wgt].sum(),
                    df.groupby(tgt)[wgt].sum()
                ]).groupby(level=0).sum()
            else:
                raise ValueError(f"Unknown degree_type: {degree_type}")
        else:
            # count of incident edges per node
            if degree_type == "OUT":
                node_vals = df[src].value_counts()
            elif degree_type == "IN":
                node_vals = df[tgt].value_counts()
            elif degree_type == "TOTAL":
                node_vals = pd.concat([
                    df[src].value_counts(),
                    df[tgt].value_counts()
                ]).groupby(level=0).sum()
            else:
                raise ValueError(f"Unknown degree_type: {degree_type}")

        # Determine threshold value
        if filter_threshold == "ABSOLUTE_THRESHOLD":
            thresh = filter_value
        elif filter_threshold == "PERCENTILE_THRESHOLD":
            thresh = np.percentile(node_vals.values, filter_value)
        else:
            raise ValueError(f"Unknown filter_threshold: {filter_threshold}")

        # Select nodes to keep
        if filter_mode == "GREATER":
            keep_nodes = node_vals[node_vals >= thresh].index
        else:
            keep_nodes = node_vals[node_vals <= thresh].index

        # Filter edges where both endpoints are in keep_nodes
        df = df[df[src].isin(keep_nodes) & df[tgt].isin(keep_nodes)]
        return NetworkPortObject(networkObj.spec, df)

    # Edge filtering
    elif filter_type == "EDGE":
        weights = df[wgt]

        # Determine threshold value
        if filter_threshold == "ABSOLUTE_THRESHOLD":
            thresh = filter_value
        elif filter_threshold == "PERCENTILE_THRESHOLD":
            thresh = np.percentile(weights.values, filter_value)
        else:
            raise ValueError(f"Unknown filter_threshold: {filter_threshold}")

        # Filter edges based on mode
        if filter_mode == "GREATER":
            df = df[weights >= thresh]
        else:
            df = df[weights <= thresh]

        return NetworkPortObject(networkObj.spec, df)

    else:
        raise ValueError(f"Unknown filter_type: {filter_type}")




