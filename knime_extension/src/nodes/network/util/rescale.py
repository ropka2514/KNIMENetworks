import pandas as pd
import numpy as np

from util.port_objects import NetworkPortObject


def identity_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Transforms a network into a binary representation of relations.
    The output is a NetworkPortObject with existing edge weights set to 1.
    """
    weight_label = networkObj.get_weight_label()
    df = networkObj.get_network()
    df[weight_label] = 1
    networkObj._network = df
    return networkObj


def min_max_rescale_transform(networkObj: NetworkPortObject, a, b) -> NetworkPortObject:
    """
    Transforms a network by rescaling the edge weights to the range [a, b].
    The output is a NetworkPortObject with rescaled edge weights.
    """
    weight_label = networkObj.get_weight_label()
    df = networkObj.get_network()
    df[weight_label] = (df[weight_label] - df[weight_label].min()) / (df[weight_label].max() - df[weight_label].min())
    df[weight_label] = df[weight_label] * (b - a) + a
    networkObj._network = df
    return networkObj

def row_normalize_transform(networkObj: NetworkPortObject, degree_type) -> NetworkPortObject:
    """
    Transforms a network by normalizing the edge weights row-wise.
    The output is a NetworkPortObject with normalized edge weights.
    """
    weight_label = networkObj.get_weight_label()
    source_label = networkObj.get_source_label()
    target_label = networkObj.get_target_label()
    df = networkObj.get_network()
    if degree_type == "OUT":
        tot = df.groupby(source_label)[weight_label].transform("sum")
        df[weight_label] = df[weight_label] / tot

    elif degree_type == "IN":
        tot = df.groupby(target_label)[weight_label].transform("sum")
        df[weight_label] = df[weight_label] / tot

    elif degree_type == "TOTAL":
        tot_out = df.groupby(source_label)[weight_label].transform("sum")
        tot_in = df.groupby(target_label)[weight_label].transform("sum")
        denom = tot_out + tot_in
        df[weight_label] = df[weight_label] / denom

    return NetworkPortObject(networkObj.spec, df)

def degree_sum_rescale_transform(networkObj: NetworkPortObject, degree_type) -> NetworkPortObject:
    """
    Normalize a network by dividing the edge weights with the degree of the edge nodes on the degree type{out, in, total}.
    d_u is the {out, in, total} strength of node u.
    w’{uv} = w{uv} / (d_u + d_v)
    The output is a NetworkPortObject with summed edge weights.
    """
    weight_label = networkObj.get_weight_label()
    source_label = networkObj.get_source_label()
    target_label = networkObj.get_target_label()
    df = networkObj.get_network()

    out_strength = df.groupby(source_label)[weight_label].sum()
    in_strength = df.groupby(target_label)[weight_label].sum()

    if degree_type == "OUT":
        d_u = df[source_label].map(out_strength).fillna(0)
        d_v = df[target_label].map(out_strength).fillna(0)
    elif degree_type == "IN":
        d_u = df[source_label].map(in_strength).fillna(0)
        d_v = df[target_label].map(in_strength).fillna(0)
    elif degree_type == "TOTAL":
        d_u = df[source_label].map(out_strength).fillna(0) + df[source_label].map(in_strength).fillna(0)
        d_v = df[target_label].map(out_strength).fillna(0) + df[target_label].map(in_strength).fillna(0)
    else:
        raise ValueError(f"Unknown degree_type: {degree_type}")

    denom = d_u + d_v
    df[weight_label] = df[weight_label] / denom.replace({0: np.nan})
    df[weight_label] = df[weight_label].fillna(0)

    return NetworkPortObject(networkObj.spec, df)


def degree_prod_rescale_transform(networkObj: NetworkPortObject, degree_type) -> NetworkPortObject:
    """
    Normalize a network by dividing the edge weights with the product of the degree of the edge nodes on the degree type{out, in, total}.
    d_u is the {out, in, total} strength of node u.
    w’{uv} = w{uv} / sqrt(d_u * d_v)
    The output is a NetworkPortObject with product edge weights.
    """
    weight_label = networkObj.get_weight_label()
    source_label = networkObj.get_source_label()
    target_label = networkObj.get_target_label()
    df = networkObj.get_network()

    out_strength = df.groupby(source_label)[weight_label].sum()
    in_strength = df.groupby(target_label)[weight_label].sum()

    if degree_type == "OUT":
        d_u = df[source_label].map(out_strength).fillna(0)
        d_v = df[target_label].map(out_strength).fillna(0)
    elif degree_type == "IN":
        d_u = df[source_label].map(in_strength).fillna(0)
        d_v = df[target_label].map(in_strength).fillna(0)
    elif degree_type == "TOTAL":
        d_u = df[source_label].map(out_strength).fillna(0) + df[source_label].map(in_strength).fillna(0)
        d_v = df[target_label].map(out_strength).fillna(0) + df[target_label].map(in_strength).fillna(0)
    else:
        raise ValueError(f"Unknown degree_type: {degree_type}")

    denom = np.sqrt(d_u * d_v)
    df[weight_label] = df[weight_label] / denom.replace({0: np.nan})
    df[weight_label] = df[weight_label].fillna(0)

    return NetworkPortObject(networkObj.spec, df)


def inverse_transform(networkObj: NetworkPortObject, epsilon) -> NetworkPortObject:
    """
    Transforms a network by inverting the edge weights.
    The output is a NetworkPortObject with inverted edge weights.
    """
    weight_label = networkObj.get_weight_label()
    df = networkObj.get_network()
    df[weight_label] = 1 / (df[weight_label] + epsilon)
    networkObj._network = df
    return networkObj


def log_transform(networkObj: NetworkPortObject, base, epsilon) -> NetworkPortObject:
    """
    Transforms a network by applying a logarithmic function to the edge weights.
    The output is a NetworkPortObject with transformed edge weights.
    """
    weight_label = networkObj.get_weight_label()
    df = networkObj.get_network()
    df[weight_label] = np.log(df[weight_label] + epsilon) / np.log(base)
    networkObj._network = df
    return networkObj