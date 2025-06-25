import knime.extension as knext

import networks_ext
import util.network_algorithms as algo
from util.port_objects import (
    NetworkPortObject,
    NetworkPortObjectSpec,
)
from util.port_types import (
    network_port_type,
)

@knext.parameter_group(label="Network Transformation Settings")
class NetworkTransformationNodeParameters:
    transform_type = knext.EnumParameter(
        label="Transformation type",
        description="Select the type of network transformation to perform.",
        enum=algo.TransformOptions,
        default_value=algo.TransformOptions.IDENTITY.name,
    )

    set_default = knext.BoolParameter(
        label="Set Default Value",
        description="Enable to set a default value for missing or undefined weights.",
        default_value=False,
    )
    default_value = knext.DoubleParameter(
        label="Default Value",
        description="Default value to use for missing or undefined weights.",
        default_value=0.0,
    ).rule(
        knext.OneOf(set_default, [True]),
        knext.Effect.SHOW,
    )

    # +-----------------------------------------------------------+
    # Parameters for k-reachability transformations
    # +-----------------------------------------------------------+
    set_k = knext.BoolParameter(
        label="Set Maximum Steps",
        description="Enable to set a maximum number of steps for K-Reachability.",
        default_value=False,
    ).rule(
        knext.OneOf(transform_type, [algo.TransformOptions.REACHABILITY.name]),
        knext.Effect.SHOW,
    )

    k_value = knext.IntParameter(
        label="Maximum Steps (k)",
        description="Maximum number of steps for K-Reachability",
        default_value=5,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.REACHABILITY.name]),
            knext.OneOf(set_k, [True]),
        ),
        knext.Effect.SHOW,
    )

    # +-----------------------------------------------------------+
    # Parameters for rescale transformations
    # +-----------------------------------------------------------+
    rescale_method = knext.EnumParameter(
        label="Rescale Method",
        description="Select the rescale method to apply.",
        enum=algo.RescaleOptions,
        default_value=algo.RescaleOptions.GLOBAL_MIN_MAX.name,
    ).rule(
        knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
        knext.Effect.SHOW,
    )
    # Parameters for min-max rescaling
    interval_a = knext.DoubleParameter(
        label="Interval A",
        description="Lower bound for min-max rescaling (default: 0.0).",
        default_value=0.0,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
            knext.OneOf(rescale_method, [algo.RescaleOptions.GLOBAL_MIN_MAX.name]),
        ),
        knext.Effect.SHOW,
    )
    interval_b = knext.DoubleParameter(
        label="Interval B",
        description="Upper bound for min-max rescaling (default: 1.0).",
        default_value=1.0,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
            knext.OneOf(rescale_method, [algo.RescaleOptions.GLOBAL_MIN_MAX.name]),
        ),
        knext.Effect.SHOW,
    )
    # Parameters for Z-Score rescaling
    handle_constant = knext.EnumParameter(
        label="Handle Constant Weights",
        description="How to handle constant weights during Z-Score rescaling.",
        enum=algo.ConstantHandlingOptions,
        default_value=algo.ConstantHandlingOptions.ERROR.name,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
            # knext.OneOf(rescale_method, [algo.RescaleOptions.ZSCORE.name]),
        ),
        knext.Effect.SHOW,
    )
    # Parameters for log rescaling
    log_base = knext.EnumParameter(
        label="Log Base",
        description="Base for logarithmic rescaling (default: e).",
        enum=algo.LogBaseOptions,
        default_value=algo.LogBaseOptions.E.name,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
            knext.OneOf(rescale_method, [algo.RescaleOptions.LOG.name]),
        ),
        knext.Effect.SHOW,
    )
    log_custom_base = knext.DoubleParameter(
        label="Custom Log Base",
        description="Custom base for logarithmic rescaling (default: 2.718).",
        default_value=2.718,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
            knext.OneOf(rescale_method, [algo.RescaleOptions.LOG.name]),
            knext.OneOf(log_base, ["custom"]),
        ),
        knext.Effect.SHOW,
    )

    # +-----------------------------------------------------------+
    # Parameters for symmetrization transformations
    # +-----------------------------------------------------------+
    symmetrization_method = knext.EnumParameter(
        label="Symmetrization Method",
        description="Select the symmetrization method to apply.",
        enum=algo.SymmetrizationOptions,
        default_value=algo.SymmetrizationOptions.SUM.name,
    ).rule(
        knext.OneOf(transform_type, [algo.TransformOptions.SYMMETRY.name]),
        knext.Effect.SHOW,
    )

    # +-----------------------------------------------------------+
    # Parameters for filtering transformations
    # +-----------------------------------------------------------+
    filter_type = knext.EnumParameter(
        label="Filter Type",
        description="Select the type of filter to apply to the network.",
        enum=algo.FilterOptions,
        default_value=algo.FilterOptions.EDGE.name,
    ).rule(
        knext.OneOf(transform_type, [algo.TransformOptions.FILTER.name]),
        knext.Effect.SHOW,
    )
    filter_threshold = knext.EnumParameter(
        label="Filter Method",
        description="Select the filtering method to apply.",
        enum=algo.ThresholdOptions,
        default_value=algo.ThresholdOptions.ABSOLUTE_THRESHOLD.name,
    ).rule(
        knext.OneOf(transform_type, [algo.TransformOptions.FILTER.name]),
        knext.Effect.SHOW,
    )
    filter_mode = knext.EnumParameter(
        label="Filter Mode",
        description="Whether to use ≥ or ≤ for filtering edges based on the selected filter type.",
        enum=algo.FilterModeOptions,
        default_value=algo.FilterModeOptions.LESS.name,
    ).rule(
        knext.OneOf(transform_type, [algo.TransformOptions.FILTER.name]),
        knext.Effect.SHOW,
    )
    strength_mode = knext.BoolParameter(
        label="Strength Mode",
        description="Check to filter based on node strength instead of degree",
        default_value=False,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.FILTER.name]),
            knext.OneOf(filter_type, [algo.FilterOptions.NODE.name]),
        ),
        knext.Effect.SHOW,
    )
    filter_value = knext.DoubleParameter(
        label="Filter Value",
        description="Value to use for filtering edges based on the selected filter type.",
        default_value=0.0,
    ).rule(
        knext.OneOf(transform_type, [algo.TransformOptions.FILTER.name]),
        knext.Effect.SHOW,
    )

    # +-----------------------------------------------------------+
    # Common Parameters for different methods
    # +-----------------------------------------------------------+
    degree_type = knext.EnumParameter(
        label="Degree Type",
        description="Type of degree to use for normalization.",
        enum=algo.DegreeTypeOptions,
        default_value=algo.DegreeTypeOptions.TOTAL.name,
    ).rule(
        knext.Or(
            knext.And(
                knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
                knext.OneOf(
                    rescale_method,
                    [
                        algo.RescaleOptions.RANDOM_WALK.name,
                        algo.RescaleOptions.DEGREE_SUM.name,
                        algo.RescaleOptions.DEGREE_PROD.name,
                        algo.RescaleOptions.SYMMETRIC.name,
                    ],
                ),
            ),
            knext.And(
                knext.OneOf(transform_type, [algo.TransformOptions.FILTER.name]),
                knext.OneOf(
                    filter_type,
                    [
                        algo.FilterOptions.NODE.name,
                    ],
                ),
            ),
        ),
        knext.Effect.SHOW,
    )
    epsilon = knext.DoubleParameter(
        label="Epsilon",
        description="Small value to avoid division by zero error in log rescaling (default: 1e-10).",
        default_value=1e-10,
    ).rule(
        knext.And(
            knext.OneOf(transform_type, [algo.TransformOptions.RESCALE.name]),
            knext.OneOf(
                rescale_method,
                [
                    algo.RescaleOptions.INVERSE.name,
                    algo.RescaleOptions.LOG.name,
                ],
            ),
        ),
        knext.Effect.SHOW,
    )

    def validate(self, values: dict):
        match values["transform_type"]:
            case algo.TransformOptions.RESCALE.name:
                a = values["interval_a"]
                b = values["interval_b"]
                if a >= b:
                    raise ValueError(
                        "For interval [a,b], a must be less than b for Min-Max rescaling."
                    )
            case algo.TransformOptions.FILTER.name:
                if values["filter_threshold"] == algo.ThresholdOptions.PERCENTILE_THRESHOLD.name and (
                    values["filter_value"] < 0 or values["filter_value"] > 1
                ):
                    raise ValueError(
                        "For absolute threshold filtering, the filter value must be non-negative."
                    )

@knext.node(
    name="Network Transformation",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/transform.png",
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
        return algo.get_transform_schema(
            input_schema,
            settings=self.settings,
        )

    def execute(
        self, exec_context: knext.ExecutionContext, input: NetworkPortObject
    ) -> NetworkPortObject:
        self.network = input.get_network()
        self.source_label = input.get_source_label()
        self.target_label = input.get_target_label()
        self.weight_label = input.get_weight_label()
        self.symmetric = input.is_symmetric()
        self.two_mode = input.is_two_mode()

        match self.settings.transform_type:
            case algo.TransformOptions.DISTANCE.name:
                return algo.distance_transform(input)
            case algo.TransformOptions.REACHABILITY.name:
                if self.settings.set_k:
                    return algo.k_reachability_transform(
                        input, max_step=self.settings.k_value
                    )
                else:
                    return algo.reachability_transform(input)
            case algo.TransformOptions.DEPENDENCY.name:
                return algo.dependency_transform(input)
            case algo.TransformOptions.MAX_FLOW.name:
                raise algo.max_flow_transform(input)
            case algo.TransformOptions.IDENTITY.name:
                return algo.identity_transform(input)
            case algo.TransformOptions.RESCALE.name:
                match self.settings.rescale_method:
                    case algo.RescaleOptions.GLOBAL_MIN_MAX.name:
                        return algo.min_max_rescale_transform(
                            input,
                            a=self.settings.interval_a,
                            b=self.settings.interval_b,
                        )
                    case algo.RescaleOptions.RANDOM_WALK.name:
                        return algo.row_normalize_transform(
                            input,
                            degree_type=self.settings.degree_type.name,
                        )
                    case algo.RescaleOptions.DEGREE_SUM.name:
                        return algo.degree_sum_rescale_transform(
                            input,
                            degree_type=self.settings.degree_type.name,
                        )
                    case algo.RescaleOptions.DEGREE_PROD.name:
                        return algo.degree_prod_rescale_transform(
                            input,
                            degree_type=self.settings.degree_type.name,
                        )
                    case algo.RescaleOptions.INVERSE.name:
                        return algo.inverse_transform(
                            input,
                            epsilon=self.settings.epsilon,
                        )
                    case algo.RescaleOptions.LOG.name:
                        return algo.log_transform(
                            input,
                            base=self.settings.log_base,
                            epsilon=self.settings.epsilon,
                        )
                    case _:
                        raise ValueError("Invalid rescale method selected.")
            case algo.TransformOptions.SYMMETRY.name:
                match self.settings.symmetrization_method:
                    case algo.SymmetrizationOptions.SUM.name:
                        return algo.sum_symmetrize_transform(input)
                    case algo.SymmetrizationOptions.AVERAGE.name:
                        return algo.average_symmetrize_transform(input)
                    case algo.SymmetrizationOptions.MAX.name:
                        return algo.max_symmetrize_transform(input)
                    case algo.SymmetrizationOptions.MIN.name:
                        return algo.min_symmetrize_transform(input)
                    case algo.SymmetrizationOptions.BIN_OR.name:
                        return algo.bin_or_symmetrize_transform(input)
                    case algo.SymmetrizationOptions.BIN_AND.name:
                        return algo.bin_and_symmetrize_transform(input)
                    case _:
                        raise ValueError("Invalid symmetrization method selected.")
            case algo.TransformOptions.FILTER.name:
                return algo.filter_transform(
                    input,
                    degree_type=self.settings.degree_type.name,
                    filter_type=self.settings.filter_type.name,
                    filter_threshold=self.settings.filter_threshold.name,
                    filter_mode=self.settings.filter_mode.name,
                    filter_value=self.settings.filter_value,
                    strength_mode=self.settings.strength_mode,
                )
            case _:
                raise ValueError("Invalid transformation type selected.")
