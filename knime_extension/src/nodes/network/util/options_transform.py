import knime_extension as knext

class TransformOptions(knext.EnumParameterOptions):
    # Walk-based transformations
    DISTANCE = (
        "Distance Transformation",
        "Compute the shortestdistance between all node pairs.",
    )
    REACHABILITY = (
        "Reachability Transformation",
        "Compute the reachability of all nodes.",
    )
    DEPENDENCY = ("Dependency Transformation", "Compute the dependency of all nodes.")
    MAX_FLOW = (
        "Max Flow Transformation",
        "Compute the maximum flow between all node pairs.",
    )

    # Neighborhood-based transformations
    IDENTITY = (
        "Identity Transformation",
        "Transform the network to represent only binary relations. Whether there is a relation or not.",
    )
    RESCALE = (
        "Rescale Transformation",
        "Rescale the network relations of each node.",
    )
    SYMMETRY = (
        "Symmetrization Transformation",
        "Symmetrize the network relations of each node.",
    )
    FILTER = (
        "Filter Transformation",
        "Filter the network relations of each node based on a condition.",
    )


class RescaleOptions(knext.EnumParameterOptions):
    GLOBAL_MIN_MAX = (
        "Min-Max",
        "Rescale linearly to the range [a, b] based on global min and max values.",
    )
    RANDOM_WALK = (
        "Random Walk",
        "Rescale based on random walk probabilities.",
    )
    SYMMETRIC = ("Symmetric", "Normalize the network symmetrically.")
    DEGREE_SUM = ("Degree Sum", "Normalize based on the degree sum.")
    DEGREE_PROD = ("Degree Product", "Normalize based on the degree product.")
    # ZSCORE = ("Z-Score", "Rescale using Z-Score normalization.")
    INVERSE = ("Inverse", "Apply inverse transformation to weights.")
    LOG = ("Logarithmic", "Apply logarithmic transformation to weights.")


class SymmetrizationOptions(knext.EnumParameterOptions):
    SUM = ("Sum", "Symmetrize by summing weights.")
    AVERAGE = ("Average", "Symmetrize by averaging weights.")
    MAX = ("Maximum", "Symmetrize by taking the maximum weight.")
    MIN = ("Minimum", "Symmetrize by taking the minimum weight.")
    BIN_OR = (
        "Binary OR",
        "Symmetrize by treating weights as binary and applying logical OR.",
    )
    BIN_AND = (
        "Binary AND",
        "Symmetrize by treating weights as binary and applying logical AND.",
    )


class FilterOptions(knext.EnumParameterOptions):
    NODE = (
        "Node Filter",
        "Filter nodes based on their degree or strength.",
    )
    EDGE = (
        "Edge Filter",
        "Filter edges based on their weights.",
    )


class ThresholdOptions(knext.EnumParameterOptions):
    ABSOLUTE_THRESHOLD = (
        "Absolute Threshold",
        "Filter  based on an absolute  threshold.",
    )
    PERCENTILE_THRESHOLD = (
        "Percentile Threshold",
        "Filter based on a percentile of weights. For example, 50 means the median weight.",
    )


class FilterModeOptions(knext.EnumParameterOptions):
    LESS = (
        "Less Than or Equal",
        "Filter edges with weights less than or equal to the specified threshold.",
    )
    GREATER = (
        "Greater Than or Equal",
        "Filter edges with weights greater than or equal to the specified threshold.",
    )


class ConstantHandlingOptions(knext.EnumParameterOptions):
    ERROR = ("Error", "Raise an error if constant weights are found.")
    ZERO = ("Zero", "Set constant weights to zero.")
    IGNORE = ("Ignore", "Ignore constant weights and rescale the rest.")


class LogBaseOptions(knext.EnumParameterOptions):
    E = ("e", "Natural logarithm (base e)")
    TEN = ("10", "Common logarithm (base 10)")
    TWO = ("2", "Binary logarithm (base 2)")
    CUSTOM = ("custom", "Custom base (enter below)")


class DegreeTypeOptions(knext.EnumParameterOptions):
    IN = ("In-Degree", "Use in-degree for normalization.")
    OUT = ("Out-Degree", "Use out-degree for normalization.")
    TOTAL = ("Total Degree", "Use total degree (in + out) for normalization.")
