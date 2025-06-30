import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from scipy.stats import spearmanr
from scipy.stats import kendalltau

# --- Configuration ---
ORIGINAL_CSV = "results_workflows/python_between.csv"  # Calculated scores
INPUT_CSV = "results_workflows/medical_between_workflow.csv"  # Positional dominance edges
CENTRALITY_COL = "BetweennessCentrality"  # Column name for centrality in original CSV

df_py = pd.read_csv(ORIGINAL_CSV) # "Node","Degree(/Betweenness)Centrality"
df_wf = pd.read_csv(INPUT_CSV) # "ID","sum_1"

df1 = df_py.rename(columns={CENTRALITY_COL: 'centrality_1'})
df2 = df_wf.rename(columns={'sum_1': 'centrality_2'})

# since knime adds "Row" in front of integer node labels, we need to rename all nodes in "Row ID" column, from "Row 1" to 1
df2['row ID'] = df2['row ID'].str.replace('Row', '').astype(int)

merged = pd.merge(df1, df2, left_on='Node', right_on='row ID')

merged['rank_1'] = merged['centrality_1'].rank(ascending=False, method='min')
merged['rank_2'] = merged['centrality_2'].rank(ascending=False, method='min')

# print the merged DataFrame, rows sorted by rank_1
print(merged.sort_values(by='rank_1'))

same_ranking = (merged['rank_1'] == merged['rank_2']).all()
print("Same ranking:", same_ranking)

corr, _ = spearmanr(merged['centrality_1'], merged['centrality_2'])
print("Spearman rank correlation:", corr)

kendall_corr, _ = kendalltau(merged['centrality_1'], merged['centrality_2'])
print("Kendall's tau correlation:", kendall_corr)


# check if 




