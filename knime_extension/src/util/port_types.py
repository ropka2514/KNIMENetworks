import knime.extension as knext
import pandas as pd
import pickle


# class AttributePortObjectSpec(knext.PortObjectSpec):
#     def __init__(self, node_column: str, attribute_column: str) -> None:
#         super().__init__()
#         self._attribute_column = attribute_column
#         self._node_column = node_column

#     def serialize(self) -> dict:
#         return {
#             "attribute_column": self._attribute_column,
#             "node_column": self._node_column,
#         }

#     @classmethod
#     def deserialize(cls, data: dict) -> "AttributePortObjectSpec":
#         return cls(data["attribute_column"], data["node_column"])

#     @property
#     def node_column(self) -> str:
#         return self._node_column

#     @property
#     def attribute_column(self) -> str:
#         return self._attribute_column


# class AttributePortObject(knext.PortObject):
#     def __init__(self, spec: AttributePortObjectSpec, attributes) -> None:
#         super().__init__(spec)
#         self._attributes = attributes

#     def serialize(self) -> bytes:
#         return pickle.dumps(self._attributes)

#     @classmethod
#     def deserialize(
#         cls, spec: AttributePortObjectSpec, data: bytes
#     ) -> "AttributePortObject":
#         attributes = pickle.loads(data)
#         return cls(spec, attributes)

#     def get_attribute(self):
#         return self._attributes


class NetworkPortObjectSpec(knext.PortObjectSpec):
    def __init__(
        self,
        two_mode: bool,
        undirected: bool = False,
        # format_graph: bool = False,
        source_label: str = None,
        target_label: str = None,
        weight_label: str = None,
        # weight_column: knext.Column = None,
    ) -> None:
        super().__init__()
        self._two_mode = two_mode
        self._undirected = undirected
        # self._format_graph = format_graph
        self._source_label = source_label
        self._target_label = target_label
        self._weight_label = weight_label
        # self._weight_column = weight_column

    def serialize(self) -> dict:
        return {
            "two_mode": self._two_mode,
            "undirected": self._undirected,
            # "format_graph": self._format_graph,
            "source_label": self._source_label,
            "target_label": self._target_label,
            "weight_label": self._weight_label,
            # "weight_column": self._weight_column,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "NetworkPortObjectSpec":
        return cls(
            data["two_mode"],
            data["undirected"],
            # data["format_graph"],
            data["source_label"],
            data["target_label"],
            data["weight_label"],
            # data["weight_column"],
        )

    @property
    def undirected(self) -> bool:
        return self._undirected

    @property
    def two_mode(self) -> bool:
        return self._two_mode

    # @property
    # def format_graph(self) -> bool:
    #     return self._format_graph

    @property
    def source_label(self) -> str:
        return self._source_label

    @property
    def target_label(self) -> str:
        return self._target_label

    @property
    def weight_label(self) -> str:
        return self._weight_label

    # @property
    # def weight_column(self) -> knext.Column:
    #     return self._weight_column


class NetworkPortObject(knext.PortObject):
    def __init__(self, spec: NetworkPortObjectSpec, network) -> None:
        super().__init__(spec)
        self._network = network

    def serialize(self) -> bytes:
        return pickle.dumps(self._network)

    @classmethod
    def deserialize(
        cls, spec: NetworkPortObjectSpec, data: bytes
    ) -> "NetworkPortObject":
        network = pickle.loads(data)
        return cls(spec, network)

    def get_network(self) -> knext.Table:
        return self._network

    def get_source_label(self) -> str:
        return self.spec.source_label

    def get_target_label(self) -> str:
        return self.spec.target_label

    def get_weight_label(self) -> str:
        return self.spec.weight_label

    # def get_weight_column(self) -> knext.KnimeType:
    #     return self.spec.weight_column

    def is_two_mode(self) -> bool:
        return self.spec.two_mode

    def is_undirected(self) -> bool:
        return self.spec.undirected

    # def is_format_graph(self) -> bool:
    #     return self.spec.format_graph


network_port_type = knext.port_type(
    name="Network Port Type",
    object_class=NetworkPortObject,
    spec_class=NetworkPortObjectSpec,
)
