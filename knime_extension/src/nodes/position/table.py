import knime.extension as knext
import pandas as pd

import networks_ext
from util.port_objects import (
    PositionPortObject,
    PositionPortObjectSpec,
)
from util.port_types import (
    position_port_type,
)

@knext.parameter_group(label="Position to Table Settings")
class PositionTableNodeParameters:
    use_default = knext.BoolParameter(
        label="Fill Missing Values",
        description="Whether to fill missing values with a default value.",
        default_value=False,
    )
    default_value = knext.DoubleParameter(
        label="Default Value",
        description="Default value to use for missing positions.",
        default_value=0.0,
    )

@knext.node(
    name="Position to Table",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/to-table.png",
)
@knext.input_port(
    name="Input Positions",
    description="Input positions to convert to table.",
    port_type=position_port_type,
)
@knext.output_table(
    name="Output Table",
    description="Output table with position data.",
)

class PositionTableNode:
    settings = PositionTableNodeParameters()

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema: PositionPortObjectSpec,
    ) -> knext.Schema:
        return None

    def execute(self, context, input: PositionPortObject) -> knext.Table:
        positions, _ = input.get_uniform_positions()
        df = pd.DataFrame.from_dict(positions, orient='index')

        if self.settings.use_default:
            df.fillna(self.settings.default_value, inplace=True)

        return knext.Table.from_pandas(df)
