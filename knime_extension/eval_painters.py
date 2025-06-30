import pandas as pd
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import os

# --- Configuration ---
ORIGINAL_CSV = "results_workflows/painter_sum.csv"  # Calculated scores
INPUT_CSV = "results_workflows/painter_perm_dom.csv"  # Positional dominance edges
OUTPUT_IMG = "dag_output.png"
GRAPHVIZ_PATH = "/opt/homebrew/bin"  # adjust if dot is elsewhere

# --- Load edge list ---
df_orig = pd.read_csv(ORIGINAL_CSV)

df = pd.read_csv(INPUT_CSV)

edges_with_scores = df.merge(df_orig, left_on='source', right_on='row ID') \
                       .rename(columns={'sum_1': 'score_source'}) \
                       .drop('row ID', axis=1)

edges_with_scores = edges_with_scores.merge(df_orig, left_on='target', right_on='row ID') \
                                     .rename(columns={'sum_1': 'score_target'}) \
                                     .drop('row ID', axis=1)

violations = edges_with_scores[
    edges_with_scores['score_source'] < edges_with_scores['score_target']
]
if not violations.empty:
    print("Violating edges:")
    print(violations[['source', 'target', 'score_source', 'score_target']])
valid = (edges_with_scores['score_source'] >= edges_with_scores['score_target']).all()

print(edges_with_scores)
print("All dominance conditions satisfied?" , valid)


G = nx.DiGraph()
G.add_edges_from(df[['source', 'target']].values)


nodes = list(G.nodes)
n = len(nodes)
total_pairs = n * (n - 1) // 2

comparable = 0
for u, v in combinations(nodes, 2):
    if nx.has_path(G, u, v) or nx.has_path(G, v, u):
        comparable += 1

comparability_ratio = comparable / total_pairs
print(f"Comparability Ratio: {comparability_ratio:.3f}")




# --- Collapse cycles (mutual edges) into equivalence classes ---
sccs = list(nx.strongly_connected_components(G))
component_map = {node: i for i, comp in enumerate(sccs) for node in comp}
label_map = {i: "\n".join(sorted(comp)) for i, comp in enumerate(sccs)}

# --- Create condensed graph (DAG of equivalence classes) ---
G_condensed = nx.condensation(G, sccs)
G_dag = nx.transitive_reduction(G_condensed)

# --- Try Graphviz layout (dot) ---
try:
    from networkx.drawing.nx_pydot import graphviz_layout
    os.environ["PATH"] = GRAPHVIZ_PATH + ":" + os.environ["PATH"]
    pos = graphviz_layout(G_dag, prog="dot")
except Exception as e:
    print(f"[WARN] Falling back to spring layout: {e}")
    pos = nx.spring_layout(G_dag, seed=42)

# --- Draw the graph ---
plt.figure(figsize=(14, 8))
nx.draw(
    G_dag,
    pos,
    labels=label_map,
    with_labels=True,
    node_color='lightgray',
    edge_color='black',
    node_size=600,
    font_size=8,
    font_weight='normal'
)
plt.axis('off')
plt.show()