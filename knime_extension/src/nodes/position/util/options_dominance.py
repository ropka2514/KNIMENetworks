import knime_extension as knext

class DominanceTypeOptions(knext.EnumParameterOptions):
    """
    Options for dominance transformations in a network.
        - Coordinate-wise (Pareto) dominance
        - Majorization dominance
        - Lexicographic dominance
        - Permutation dominance
        - Neighborhood dominance
    """
    COORDINATE = (
        "Coordinate Dominance",
        "Compute the coordinate-wise (Pareto) dominance network of positions.",
    )
    MAJORIZATION = (
        "Majorization Dominance",
        "Compute the majorization dominance network of positions.",
    )
    LEXICOGRAPHIC = (
        "Lexicographic Dominance",
        "Compute the lexicographic dominance network of positions.",
    )
    PERMUTATION = (
        "Permutation Dominance",
        "Compute the permutation dominance network of positions.",
    )
    NEIGHBORHOOD = (
        "Neighborhood Dominance",
        "Compute the neighborhood dominance network of positions.",
    )

class DominanceStrictOptions(knext.EnumParameterOptions):
    """
    Options for the type of dominance to compute.
        - Strict dominance
        - Weak dominance
    """
    STRICT = (
        "Strict Dominance",
        "Compute strict dominance relations. Requires at least one strict inequality in all dimensions.",
    )
    WEAK = (
        "Weak Dominance",
        "Compute weak dominance relations.",
    )   

class DominanceDirectionOptions(knext.EnumParameterOptions):
    """
    Options for the direction of comparison in dominance relations.
        - Forward comparison
        - Backward comparison
    """
    GREATER_THAN = (
        "Greater Than",
        "larger coordinates are considered dominating",
    )
    LESS_THAN = (
        "Less Than",
        "smaller coordinates are considered dominating",
    )

class SortingDirectionOptions(knext.EnumParameterOptions):
    """
    Options for the sorting direction in dominance relations.
        - Ascending
        - Descending
    """
    ASCENDING = (
        "Ascending",
        "Sort positions in ascending order before computing dominance.",
    )
    DESCENDING = (
        "Descending",
        "Sort positions in descending order before computing dominance.",
    )

    