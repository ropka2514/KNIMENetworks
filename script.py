import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. Load edge list from CSV (adjust filename and column names as needed)
df = pd.read_csv("Test_Network_Edge_List.csv")  # df must have at least 'source' and 'target' columns

# 2. Create a NetworkX graph from the DataFrame
#    edge_attr=True pulls in any additional columns as edge attributes
G = nx.from_pandas_edgelist(df, source="source", target="target", edge_attr=True, create_using=nx.DiGraph()) 

# 3. Compute node positions using a spring (force-directed) layout
pos = nx.spring_layout(G)  

# 4. Draw the graph
plt.figure(figsize=(8, 6))
nx.draw(
    G,
    pos,
    with_labels=True,     # show node labels
    node_size=300,        # size of nodes
    edge_color="gray"     # color of edges
)
plt.title("Network Visualization")
plt.axis('off')          # turn off axis
plt.show()