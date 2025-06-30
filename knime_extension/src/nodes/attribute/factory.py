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
    Options for handling string column in the attribute factory.
    """
    # KEEP = "Keep values as is"
    BINARY = (
        "Binary relations", 
        "Convert to binary, existing values will be lost,replace with 1 for existance of attribute"
        )
    ONE_HOT = (
        "One-hot encoding", 
        "Convert to one-hot encoding, column with binary values for each unique attribute value"
        )


@knext.parameter_group(label="Attribute Settings")
class AttributeSettings:
    node_label = knext.ColumnParameter(
        label="Nodes column",
        description="Select the column with the nodes labels.",
    )
    attribute_labels = knext.MultiColumnParameter(
        label="Attribute columns",
        description="Select the column(s) with the attribute values.",
    )
    string_handling = knext.EnumParameter(
        label="String Handling, only applicable if attribute column contains string values",
        description="How to handle string attributes.",
        enum=StringHandlingOptions,
        default_value=StringHandlingOptions.BINARY.name,
    )


@knext.node(
    name="Attribute Creation",
    node_type=knext.NodeType.MANIPULATOR,
    category=networks_ext.attribute_category,
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
class AttributeFactoryNode:
    settings = AttributeSettings()

    def configure(
        self, configure_context: knext.ConfigurationContext, input_schema: knext.Schema
    ) -> AttributePortObjectSpec:
        # Check if the parameters are set
        if not self.settings.node_label:
            raise knext.InvalidParametersError("Node column must be set.")
        if not self.settings.attribute_labels:
            raise knext.InvalidParametersError("Attribute column must be set.")
        if self.settings.node_label in self.settings.attribute_labels:
            raise knext.InvalidParametersError(
                "Node column must be different from attribute column."
            )
        return AttributePortObjectSpec(
            node_column=self.settings.node_label,
            attribute_column=self.settings.attribute_labels,
        )

    def execute(
        self, exec_context: knext.ExecutionContext, input_table: knext.Table
    ) -> AttributePortObject:
        if self.settings.node_label not in input_table.column_names:
            raise knext.InvalidParametersError(
                f"Node column '{self.settings.node_label}' not found in input table."
            )
        
        df = input_table.to_pandas()
        df = df[[self.settings.node_label] + self.settings.attribute_labels]
        attr = []

        result_df = df[[self.settings.node_label]].copy()

        for col in self.settings.attribute_labels:
            if pd.api.types.is_string_dtype(df[col]):
                if self.settings.string_handling == StringHandlingOptions.BINARY:
                    result_df[col] = (df[col].notna() & (df[col] != "")).astype(int)
                    attr.append(col)
                elif self.settings.string_handling == StringHandlingOptions.ONE_HOT:
                    dummies = pd.get_dummies(df[col], prefix=col, prefix_sep="_")
                    result_df = pd.concat([result_df, dummies], axis=1)
                    attr.extend(dummies.columns.tolist())
            else:
                result_df[col] = df[col]
                attr.append(col)

        if not attr:
            attr = self.settings.attribute_labels

        return AttributePortObject(
            spec=AttributePortObjectSpec(
                node_column=self.settings.node_label,
                attribute_column=attr,
            ),
            data=result_df,
            attributes=attr,
        )