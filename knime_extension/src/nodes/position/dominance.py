import knime.extension as knext
import networks_ext
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
    PositionPortObject,
    PositionPortObjectSpec,
)
from util.port_types import (
    network_port_type,
    position_port_type,
)
from util.position_algorithms import (
    DominanceTypeOptions,
    DominanceStrictOptions,
    DominanceDirectionOptions,
    SortingDirectionOptions,
    coordinate_dominance,
    majorization_dominance,
    lexicographic_dominance,
)


@knext.parameter_group(label="Dominance Options")
class DominanceParameters:
    """
    Parameters for computing position dominance in a network.
    """

    dominance_type = knext.EnumParameter(
        label="Dominance Type",
        description="Type of dominance to compute.",
        enum=DominanceTypeOptions,
        default_value=DominanceTypeOptions.COORDINATE.name,
    )

    optional_sorting = knext.BoolParameter(
        label="Sort Positions",
        description="Whether to sort positions before computing dominance.",
        default_value=False,
    ).rule(
        knext.OneOf(
            dominance_type,
            [
             DominanceTypeOptions.LEXICOGRAPHIC.name
                ],
        ),
        knext.Effect.SHOW,
    )

    sorting_direction = knext.EnumParameter(
        label="Sorting Direction",
        description="Direction of sorting for majorization dominance.",
        enum=SortingDirectionOptions,
        default_value=SortingDirectionOptions.DESCENDING.name,
    ).rule(
        knext.Or(
            knext.And(
                knext.OneOf(dominance_type, [DominanceTypeOptions.LEXICOGRAPHIC.name]),
                knext.OneOf(optional_sorting, [True]),
            ),
            knext.OneOf(
                dominance_type,
                [DominanceTypeOptions.MAJORIZATION.name],
            ),
        ),
        knext.Effect.SHOW,
    )

    dominance_direction = knext.EnumParameter(
        label="Comparison Direction",
        description="Direction of comparison for dominance relations.",
        enum=DominanceDirectionOptions,
        default_value=DominanceDirectionOptions.GREATER_THAN.name,
    )

    dominance_strict = knext.EnumParameter(
        label="Dominance Strictness",
        description="Type of dominance to compute (strict or weak).",
        enum=DominanceStrictOptions,
        default_value=DominanceStrictOptions.WEAK.name,
    )

    set_default = knext.BoolParameter(
        label="Set Default Value",
        description="Set a default value for undefined coordinate values.",
        default_value=False,
    ).rule(
        knext.OneOf(
            dominance_type,
            [DominanceTypeOptions.COORDINATE.name,
             DominanceTypeOptions.LEXICOGRAPHIC.name,
             DominanceTypeOptions.PERMUTATION.name,
             DominanceTypeOptions.NEIGHBORHOOD.name]
        ),
        knext.Effect.SHOW,
    )

    default_value = knext.DoubleParameter(
        label="Default Value",
        description="Default value for missing dimensions (optional).",
        default_value=0.0,
    ).rule(
        knext.Or(
            knext.OneOf(dominance_type, [DominanceTypeOptions.MAJORIZATION.name]),
            knext.OneOf(set_default, [True]),
        ),
        knext.Effect.SHOW
    )


@knext.node(
    name="Position Dominances",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/dominance.png",
)
@knext.input_port(
    name="Input Positions",
    description="Input positions to compute dominance.",
    port_type=position_port_type,
)
@knext.output_port(
    name="Output Network",
    description="Output network with position dominance.",
    port_type=network_port_type,
)
class PositionDominanceNode(knext.PythonNode):
    settings = DominanceParameters()

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema: PositionPortObjectSpec,
    ) -> NetworkPortObjectSpec:
        return NetworkPortObjectSpec(
            source_label=input_schema.node_column,
            target_label="node_j",
            weight_label="dominates",
            symmetric=False,
            two_mode=False,
        )

    def execute(self, context, input: PositionPortObject) -> NetworkPortObject:
        match self.settings.dominance_type:
            case DominanceTypeOptions.COORDINATE.name:
                return coordinate_dominance(
                    input,
                    self.settings.dominance_strict,
                    self.settings.dominance_direction,
                    self.settings.default_value if self.settings.set_default else None,
                )
            case DominanceTypeOptions.MAJORIZATION.name:
                return majorization_dominance(
                    input,
                    self.settings.dominance_strict,
                    self.settings.dominance_direction,
                    self.settings.sorting_direction,
                    self.settings.default_value,
                )
            case DominanceTypeOptions.LEXICOGRAPHIC.name:
                return lexicographic_dominance(
                    input,
                    self.settings.dominance_strict,
                    self.settings.dominance_direction,
                    self.settings.sorting_direction if self.settings.optional_sorting else None,
                    self.settings.default_value,
                )
            case DominanceTypeOptions.PERMUTATION.name:
                raise NotImplementedError(
                    "Permutation dominance is not yet implemented."
                )
            case DominanceTypeOptions.NEIGHBORHOOD.name:
                raise NotImplementedError(
                    "Neighborhood dominance is not yet implemented."
                )   
