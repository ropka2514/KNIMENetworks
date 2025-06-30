import knime.extension as knext
import pandas as pd
import pickle

# +---------------------------------------------------------------------------
# | PositionPortObjectSpec and PositionPortObject
# +---------------------------------------------------------------------------
class PositionPortObjectSpec(knext.PortObjectSpec):
    def __init__(self, node_column: str) -> None:
        super().__init__()
        self._node_column = node_column

    def serialize(self) -> dict:
        return {
            "node_column": self._node_column,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "PositionPortObjectSpec":
        return cls(data["node_column"])

    @property
    def node_column(self) -> str:
        return self._node_column


class PositionPortObject(knext.PortObject):
    def __init__(
        self,
        spec: PositionPortObjectSpec,
        positions,
    ) -> None:
        super().__init__(spec)
        self._positions = positions

    def serialize(self) -> bytes:
        return pickle.dumps((self._positions))

    @classmethod
    def deserialize(
        cls, spec: PositionPortObjectSpec, data: bytes
    ) -> "PositionPortObject":
        positions = pickle.loads(data)
        return cls(spec, positions)

    def get_positions(self):
        return self._positions
    
    def get_uniform_positions(self):
        dfs = [
            pd.DataFrame(d).T.add_suffix(f'_{i}')
            for i, (d,_,_) in enumerate(self._positions, start=1)
        ]
        df = pd.concat(dfs, axis=1)
        dict = df.to_dict(orient='index')
        clean_data = {
            node: {
                coord_name: coord_val
                for coord_name, coord_val in coords.items()
                if pd.notna(coord_val)
            }
            for node, coords in dict.items()
        }

        return (clean_data, set(df.columns.tolist()))


# +---------------------------------------------------------------------------
# | AttributePortObjectSpec and AttributePortObject
# +---------------------------------------------------------------------------
class AttributePortObjectSpec(knext.PortObjectSpec):
    def __init__(self, node_column: str, attribute_column: str) -> None:
        super().__init__()
        self._node_column = node_column
        self._attribute_column = attribute_column

    def serialize(self) -> dict:
        return {
            "node_column": self._node_column,
            "attribute_column": self._attribute_column,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "AttributePortObjectSpec":
        return cls(data["node_column"], data["attribute_column"])

    @property
    def node_column(self) -> str:
        return self._node_column
    @property
    def attribute_column(self) -> str:
        return self._attribute_column


class AttributePortObject(knext.PortObject):
    def __init__(self, spec: AttributePortObjectSpec, attributes, data) -> None:
        super().__init__(spec)
        self._attributes = attributes
        self._data = data

    def serialize(self) -> bytes:
        # Serialize both the attributes list and the DataFrame
        return pickle.dumps((self._attributes, self._data))

    @classmethod
    def deserialize(
        cls, spec: AttributePortObjectSpec, data: bytes
    ) -> "AttributePortObject":
        attributes, df = pickle.loads(data)
        return cls(spec, attributes, df)

    def get_data(self) -> pd.DataFrame:
        return self._data

    def get_attributes(self):
        return self._attributes

# +---------------------------------------------------------------------------
# | NetworkPortObjectSpec and NetworkPortObject
# +---------------------------------------------------------------------------
class NetworkPortObjectSpec(knext.PortObjectSpec):
    def __init__(
        self,
        two_mode: bool,
        symmetric: bool = False,
        irreflexive: bool = True,
        source_label: str = None,
        target_label: str = None,
        weight_label: str = None,
    ) -> None:
        super().__init__()
        self._two_mode = two_mode
        self._symmetric = symmetric
        self._irreflexive = irreflexive
        self._source_label = source_label
        self._target_label = target_label
        self._weight_label = weight_label

    def serialize(self) -> dict:
        return {
            "two_mode": self._two_mode,
            "symmetric": self._symmetric,
            "irreflexive": self._irreflexive,
            "source_label": self._source_label,
            "target_label": self._target_label,
            "weight_label": self._weight_label,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "NetworkPortObjectSpec":
        return cls(
            data["two_mode"],
            data["symmetric"],
            data["irreflexive"],
            data["source_label"],
            data["target_label"],
            data["weight_label"],
        )

    @property
    def symmetric(self) -> bool:
        return self._symmetric

    @property
    def irreflexive(self) -> bool:
        return self._irreflexive

    @property
    def two_mode(self) -> bool:
        return self._two_mode

    @property
    def source_label(self) -> str:
        return self._source_label

    @property
    def target_label(self) -> str:
        return self._target_label

    @property
    def weight_label(self) -> str:
        return self._weight_label


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

    # network contains a Dataframe edge list of the network
    def get_network(self) -> pd.DataFrame:
        return self._network

    def get_source_label(self) -> str:
        return self.spec.source_label

    def get_target_label(self) -> str:
        return self.spec.target_label

    def get_weight_label(self) -> str:
        return self.spec.weight_label

    def is_two_mode(self) -> bool:
        return self.spec.two_mode

    def is_symmetric(self) -> bool:
        return self.spec.symmetric

    def is_irreflexive(self) -> bool:
        return self.spec.irreflexive




