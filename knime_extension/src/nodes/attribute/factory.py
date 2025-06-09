import knime.extension as knext
import pandas as pd

import networks_ext
from util.port_objects import (
    AttributePortObject,
    AttributePortObjectSpec,
)
from util.port_types import (
    attribute_port_type,
)


class StringHandlingOptions(knext.EnumParameterOptions):
    """
    Options for handling string column in the network factory.
    """
    # KEEP = "Keep values as is"
    BINARY = "Convert to binary, existing values will be lost,replace with 1 for existance of attribute"
    ONE_HOT = "Convert to one-hot encoding, column with binary values for each unique attribute value"


@knext.parameter_group(label="Network Settings")
class NetworkSettings:
    node_label = knext.ColumnParameter(
        label="Nodes column",
        description="Select the column with the nodes labels.",
    )
    attribute_label = knext.ColumnParameter(
        label="Attribute column",
        description="Select the column with the attribute values.",
    )
    string_handling = knext.EnumParameter(
        label="String Handling",
        description="How to handle string attributes.",
        options=StringHandlingOptions,
        default_value=StringHandlingOptions.KEEP,
    )


@knext.node(
    name="Attribute Creation",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.main_category,
    icon_path="icons/icon-missing.png",
)
@knext.input_table(
    name="Input Table",
    description="Table of network node attributes.",
)
@knext.output_port(
    name="Output Attributes",
    description="Attribute object created from the table.",
    port_type=attribute_port_type,
)
class NetworkFactoryNode:
    settings = NetworkSettings()

    def configure(
        self, configure_context: knext.ConfigurationContext, input_schema: knext.Schema
    ) -> AttributePortObjectSpec:
        # Check if the parameters are set
        if not self.settings.node_label:
            raise knext.InvalidParametersError("Node column must be set.")
        if not self.settings.attribute_label:
            raise knext.InvalidParametersError("Attribute column must be set.")
        if self.settings.node_label == self.settings.attribute_label:
            raise knext.InvalidParametersError(
                "Node column must be different from attribute column."
            )
        return AttributePortObjectSpec(
            node_column=self.settings.node_label,
        )

    def execute(
        self, exec_context: knext.ExecutionContext, input_table: knext.Table
    ) -> AttributePortObject:
        if self.settings.node_label not in input_table.columns:
            raise knext.InvalidParametersError(
                f"Node column '{self.settings.node_label}' not found in input table."
            )
        if self.settings.attribute_label not in input_table.columns:
            raise knext.InvalidParametersError(
                f"Attribute column '{self.settings.attribute_label}' not found in input table."
            )
        
        df = input_table.to_pandas()
        df = df[[self.settings.node_label, self.settings.attribute_label]]
        attr = []

        if pd.api.types.is_string_dtype(df[self.settings.attribute_label]):
            if self.settings.string_handling == StringHandlingOptions.BINARY:
                df[self.settings.attribute_label] = 1
            elif self.settings.string_handling == StringHandlingOptions.ONE_HOT:
                df = pd.get_dummies(
                    df,
                    columns=[self.settings.attribute_label],
                    prefix=self.settings.attribute_label,
                    prefix_sep="_",
                )
                attr = [
                    col for col in df.columns if col.startswith(self.settings.attribute_label + "_")
                ]
    
        if attr == []:
            attr = [self.settings.attribute_label]
        return AttributePortObject(
            spec=AttributePortObjectSpec(
                node_column=self.settings.node_label,
                attribute_column=self.settings.attribute_label,
            ),
            data=df,
            attributes=attr,
        )
