from collections import defaultdict
import pandas as pd
from util.port_objects import (
    NetworkPortObject,
    PositionPortObject,
    PositionPortObjectSpec,
    AttributePortObject
)

#+-------------------------------------------------------------+
#| Position Factory                                            |
#+-------------------------------------------------------------+
def create_positions(input_networks: list[NetworkPortObject], input_attributes: list[AttributePortObject], str_mode) -> PositionPortObject:
    processed_networks: list[NetworkPortObject] = []
    for net in input_networks:
        weight_label = net.spec.weight_label
        df_orig = net.get_network()
        if not pd.api.types.is_numeric_dtype(df_orig[weight_label]):
            if str_mode == "BINARY":
                df_new = df_orig.copy()
                df_new[weight_label] = 1
                processed_networks.append(NetworkPortObject(spec=net.spec, network=df_new))
                continue
            elif str_mode == "ONE_HOT":
                for rel in df_orig[weight_label].unique():
                    df_rel = df_orig[df_orig[weight_label] == rel].copy()
                    # Preserve the category for labeling
                    df_rel["category"] = rel
                    df_rel[weight_label] = 1
                    processed_networks.append(NetworkPortObject(spec=net.spec, network=df_rel))
                continue
            else:
                raise ValueError(f"Unknown str_mode: {str_mode}.")
        processed_networks.append(net)

    input_networks = processed_networks
    all_pos = []

    for input_network in input_networks:
        pos = defaultdict(dict)
        dims = set()
        source_label = input_network.spec.source_label
        target_label = input_network.spec.target_label
        weight_label = input_network.spec.weight_label


        df_net = input_network.get_network()
        print(df_net)
        df_net = df_net.copy()

        
        if input_network.spec.symmetric:
            # Determine columns to include in reversed DataFrame
            cols = [source_label, target_label, weight_label]
            if "category" in df_net.columns:
                cols.append("category")
                df_rev = df_net[cols].rename(
                    columns={source_label: target_label, target_label: source_label}
                )
            df_net = pd.concat([df_net, df_rev], ignore_index=True)

        df_net["dim"] = (
            df_net[target_label].astype(str)
            + (("_" + df_net["category"])if "category" in df_net.columns else "")
        )
        
        pivot = df_net.pivot_table(
            index=source_label,
            columns="dim",
            values=weight_label,
            aggfunc="first",
        )
        for src, row in pivot.iterrows():
            for dim, val in row.dropna().items():
                pos[src][dim] = val
                dims.add(dim)

        pos = dict(pos)
        dims = list(dims)
        all_pos.append((pos, dims, weight_label))

    for input_attribute in input_attributes:
        weight_label = input_attribute.spec.attribute_column
        df = input_attribute.get_data()
        attr = input_attribute.get_attributes()
        pos = df.to_dict(orient="index")
        all_pos.append((pos, attr, weight_label))

    print(all_pos[0][0])

    spec = PositionPortObjectSpec(node_column='node')

    return PositionPortObject(
        spec=spec,
        positions=all_pos,
    )