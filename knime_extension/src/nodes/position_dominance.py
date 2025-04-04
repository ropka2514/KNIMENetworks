import knime.extension as knext
import pandas as pd
import networkx as nx
import numpy as np

import networks_ext
from util.port_types import (
    NetworkPortObject,
    NetworkPortObjectSpec,
    network_port_type,
)


@knext.node(
    name="Node Position Dominance",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_table(
    name="Input Network",
    description="Input network to compute positions.",
)
@knext.output_table(
    name="Output Table",
    description="Output table with network positions.",
)
class PositionDominanceNode:
    #  TODO: add neutral value for nonexistent edges

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema: knext.Schema,
    ) -> knext.Schema:
        # ktype1 = knext.string()
        # ktype2 = input_schema.weight_column.ktype
        # return knext.Schema([ktype1,ktype1, ktype2],[input_schema.source_label, input_schema.target_label, input_schema.weight_label])
        return None

    def execute(self, context, input_table: knext.Table) -> knext.Table:
        matrix = input_table.to_pandas()
        M = matrix.to_numpy()
        n = M.shape[0]
        nodes = np.array(matrix.index)

        M_i = M[:, np.newaxis, :]
        M_j = M[np.newaxis, :, :]

        mask = np.ones((n, n, n), dtype=bool)
        for j in range(n):
            mask[:, j, j] = False

        comparison = (M_i <= M_j) | ~mask
        dominance_matrix = np.all(comparison, axis=2).astype(int)

        i_idx, j_idx = np.where(~np.eye(n, dtype=bool))
        dominance_df = pd.DataFrame(
            {
                "node_i": nodes[i_idx],
                "node_j": nodes[j_idx],
                "dominates": dominance_matrix[i_idx, j_idx],
            }
        )

        return knext.Table.from_pandas(dominance_df)
