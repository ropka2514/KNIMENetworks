import knime.extension as knext

import networks_ext
import util.position_algorithms as algo
from util.port_objects import (
    PositionPortObject,
    PositionPortObjectSpec,
)
from util.port_types import (
    position_port_type,
)


class PositionTransformOptions(knext.EnumParameterOptions):
    SUM = ("Sum Transform", "Sum all coordinates for every node position.")
    EUCLIDEAN_NORM = (
        "Euclidean Norm Transform",
        "Compute the Euclidean norm for every node position.",
    )
    MANHATTAN_NORM = (
        "Manhattan Norm Transform",
        "Compute the Manhattan norm for every node position.",
    )
    AVERAGE = (
        "Average Transform",
        "Compute the average of all coordinates for every node position.",
    )
    MAX = ("Max Transform", "Compute the maximum coordinate for every node position.")
    MIN = ("Min Transform", "Compute the minimum coordinate for every node position.")
    INVERSE = (
        "Inverse Transform",
        "Compute the inverse of all the coordinates for every node position.",
    )
    LOG = (
        "Log Transform",
        "Compute the logarithm of all the coordinates for every node position.",
    )
    ZSCORE = (
        "Z-Score Transform",
        "Compute the Z-Score normalization for every node coordinate.",
    )


@knext.parameter_group(label="Network Transformation Settings")
class PositionTransformationNodeParameters:
    transform_type = knext.EnumParameter(
        label="Transformation type",
        description="Select the type of transformation to perform on the node positions.\nAfter selection, reopen the configuration window to set transformation parameters.",
        enum=PositionTransformOptions,
        default_value=PositionTransformOptions.SUM.name,
    )
    use_default = knext.BoolParameter(
        label="Use Default Settings",
        description="Whether to use default value for missing/undefined positions.",
        default_value=False,
    )
    default_value = knext.DoubleParameter(
        label="Default Value",
        description="Default value to use for missing/undefined positions.",
        default_value=0.0,
    )


@knext.node(
    name="Position Transformation",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/transform.png",
)
@knext.input_port(
    name="Input Position",
    description="Input positions to transform.",
    port_type=position_port_type,
)
@knext.output_port(
    name="Output Position",
    description="Output transformed positions.",
    port_type=position_port_type,
)
class PositionTransformationNode(knext.PythonNode):
    settings = PositionTransformationNodeParameters()

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema: PositionPortObjectSpec,
    ) -> PositionPortObjectSpec:
        return PositionPortObjectSpec(
            node_column=input_schema.node_column,
        )

    def execute(
        self, exec_context: knext.ExecutionContext, input: PositionPortObject
    ) -> PositionPortObject:
        match self.settings.transform_type:
            case PositionTransformOptions.SUM.name:
                return algo.sum_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case PositionTransformOptions.EUCLIDEAN_NORM.name:
                return algo.euclidean_norm_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case PositionTransformOptions.MANHATTAN_NORM.name:
                return algo.manhattan_norm_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case PositionTransformOptions.AVERAGE.name:
                return algo.average_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case PositionTransformOptions.MAX.name:
                return algo.max_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case PositionTransformOptions.MIN.name:
                return algo.min_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case PositionTransformOptions.INVERSE.name:
                # TODO: Implement custom epsilon handling for inverse transform
                return algo.inverse_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                    epsilon=1e-6,
                )
            case PositionTransformOptions.LOG.name:
                return algo.log_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case PositionTransformOptions.ZSCORE.name:
                return algo.zscore_transform(
                    input,
                    self.settings.default_value if self.settings.use_default else None,
                )
            case _:
                raise ValueError("Invalid transformation type selected.")
