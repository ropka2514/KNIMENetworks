import knime.extension as knext
import networkx as nx
import pandas as pd

import networks_ext
from util.port_types import (
    NetworkPortObject,
    NetworkPortObjectSpec,
    network_port_type,
)


class TransformOptions(knext.EnumParameterOptions):
    DISTANCE = ("Distance Transform", "Compute the distance between all nodes.")
    PROJECTION = ("One-Mode Projection", "Project a two-mode network to one-mode.")


@knext.parameter_group(label="Network Transformation Settings")
class NetworkTransformationNodeParameters:
    transform_type = knext.EnumParameter(
        label="Transformation type",
        description="Select the type of network transformation to perform.",
        enum=TransformOptions,
        default_value=TransformOptions.DISTANCE.name,
    )


@knext.node(
    name="Network Transformation",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_port(
    name="Input Network",
    description="Input network to transform.",
    port_type=network_port_type,
)
@knext.output_port(
    name="Output Network",
    description="Output transformed network.",
    port_type=network_port_type,
)
class NetworkTransformationNode(knext.PythonNode):
    settings = NetworkTransformationNodeParameters()

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema: NetworkPortObjectSpec,
    ) -> NetworkPortObjectSpec:
        match self.settings.transform_type:
            case TransformOptions.DISTANCE.name:
                if input_schema.two_mode:
                    raise ValueError("Input must be one-mode.")
                return NetworkPortObjectSpec(
                    source_label=input_schema.source_label,
                    target_label=input_schema.target_label,
                    weight_label="distance",
                    undirected=input_schema.undirected,
                    two_mode=False,
                )
        raise ValueError("Invalid transformation type selected.")

    def execute(
        self, exec_context: knext.ExecutionContext, input: NetworkPortObject
    ) -> NetworkPortObject:
        self.network = input.get_network()
        self.source_label = input.get_source_label()
        self.target_label = input.get_target_label()
        self.weight_label = input.get_weight_label()
        self.undirected = input.is_undirected()
        self.two_mode = input.is_two_mode()

        match self.settings.transform_type:
            case TransformOptions.DISTANCE.name:
                return self.distance_transform()

        raise ValueError("Invalid transformation type selected.")

    def distance_transform(self) -> NetworkPortObject:
        if self.two_mode:
            raise ValueError(
                "Distance transform is not supported for two-mode networks. Consider projection to one-mode network."
            )
        df = self.network.to_pandas()
        if not pd.api.types.is_numeric_dtype(df[self.weight_label]):
            raise ValueError("Weight column must be numeric.")
        if (df[self.weight_label] <= 0).any():
            raise ValueError("Weight column must be positive.")

        G = nx.from_pandas_edgelist(
            df,
            source=self.source_label,
            target=self.target_label,
            edge_attr=self.weight_label,
            create_using=nx.Graph() if self.undirected else nx.DiGraph(),
        )

        all_pairs_distances = dict(
            nx.all_pairs_dijkstra_path_length(G, weight=self.weight_label)
        )
        edges = [
            (source, target, distance)
            for source, targets in all_pairs_distances.items()
            for target, distance in targets.items()
            if source != target
        ]
        df = pd.DataFrame(
            edges, columns=[self.source_label, self.target_label, "distance"]
        )
        if self.undirected:
            df_sorted = df.apply(
                lambda row: sorted([row[self.source_label], row[self.target_label]])
                + [row["distance"]],
                axis=1,
                result_type="expand",
            )
            df_sorted.columns = [self.source_label, self.target_label, "distance"]
            df_sorted = df_sorted.drop_duplicates()
            df = df_sorted

        # Create a new NetworkPortObjectSpec with the updated columns
        return NetworkPortObject(
            NetworkPortObjectSpec(
                source_label=self.source_label,
                target_label=self.target_label,
                weight_label="distance",
                undirected=self.undirected,
                two_mode=self.two_mode,
            ),
            knext.Table.from_pandas(df),
        )
