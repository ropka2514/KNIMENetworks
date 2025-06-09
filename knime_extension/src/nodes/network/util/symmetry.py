import pandas as pd
from util.port_objects import NetworkPortObject

def sum_symmetrize_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Symmetrize by taking the maximum weight among directed pairs.
    w'_{uv} = w_{uv} + w_{vu}
    """
    src = networkObj.get_source_label()
    tgt = networkObj.get_target_label()
    wgt = networkObj.get_weight_label()
    df = networkObj.get_network()[[src, tgt, wgt]].copy()  

    df['pair'] = df.apply(lambda r: tuple(sorted((r[src], r[tgt]))), axis=1)
    agg = df.groupby('pair')[wgt].sum().reset_index()
    pairs = pd.DataFrame(agg['pair'].tolist(), columns=[src, tgt])
    pairs[wgt] = agg[wgt]
    return NetworkPortObject(networkObj.spec, pairs)

def average_symmetrize_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Symmetrize by averaging weights of directed pairs.
    w'_{uv} = 0.5 * (w_{uv} + w_{vu})
    """
    src = networkObj.get_source_label()
    tgt = networkObj.get_target_label()
    wgt = networkObj.get_weight_label()
    df = networkObj.get_network()[[src, tgt, wgt]].copy()
    df['pair'] = df.apply(lambda r: tuple(sorted((r[src], r[tgt]))), axis=1)
    agg = df.groupby('pair')[wgt].mean().reset_index()
    pairs = pd.DataFrame(agg['pair'].tolist(), columns=[src, tgt])
    pairs[wgt] = agg[wgt]
    return NetworkPortObject(networkObj.spec, pairs)

def max_symmetrize_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Symmetrize by taking the maximum weight among directed pairs.
    w'_{uv} = max(w_{uv}, w_{vu}).
    """
    src = networkObj.get_source_label()
    tgt = networkObj.get_target_label()
    wgt = networkObj.get_weight_label()
    df = networkObj.get_network()[[src, tgt, wgt]].copy()
    df['pair'] = df.apply(lambda r: tuple(sorted((r[src], r[tgt]))), axis=1)
    agg = df.groupby('pair')[wgt].max().reset_index()
    pairs = pd.DataFrame(agg['pair'].tolist(), columns=[src, tgt])
    pairs[wgt] = agg[wgt]
    return NetworkPortObject(networkObj.spec, pairs)

def min_symmetrize_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Symmetrize by taking the minimum weight among directed pairs.
    w'_{uv} = min(w_{uv}, w_{vu})
    """
    src = networkObj.get_source_label()
    tgt = networkObj.get_target_label()
    wgt = networkObj.get_weight_label()
    df = networkObj.get_network()[[src, tgt, wgt]].copy()
    df['pair'] = df.apply(lambda r: tuple(sorted((r[src], r[tgt]))), axis=1)
    agg = df.groupby('pair')[wgt].min().reset_index()
    pairs = pd.DataFrame(agg['pair'].tolist(), columns=[src, tgt])
    pairs[wgt] = agg[wgt]
    return NetworkPortObject(networkObj.spec, pairs)

def bin_or_symmetrize_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Binary OR symmetrization: include an undirected edge if at least one directed edge exists.
    """
    src = networkObj.get_source_label()
    tgt = networkObj.get_target_label()
    df = networkObj.get_network()[[src, tgt]].drop_duplicates().copy()
    df['pair'] = df.apply(lambda r: tuple(sorted((r[src], r[tgt]))), axis=1)
    df = df.drop_duplicates('pair')
    pairs = pd.DataFrame(df['pair'].tolist(), columns=[src, tgt])
    pairs[networkObj.get_weight_label()] = 1
    return NetworkPortObject(networkObj.spec, pairs)

def bin_and_symmetrize_transform(networkObj: NetworkPortObject) -> NetworkPortObject:
    """
    Binary AND symmetrization: include an undirected edge only if both directed edges exist.
    """
    src = networkObj.get_source_label()
    tgt = networkObj.get_target_label()
    df = networkObj.get_network()[[src, tgt]].copy()
    df['pair'] = df.apply(lambda r: tuple(sorted((r[src], r[tgt]))), axis=1)
    counts = df.groupby('pair').size().reset_index(name='count')
    valid = counts[counts['count'] >= 2]['pair'].tolist()
    pairs = pd.DataFrame(valid, columns=[src, tgt])
    pairs[networkObj.get_weight_label()] = 1
    return NetworkPortObject(networkObj.spec, pairs)