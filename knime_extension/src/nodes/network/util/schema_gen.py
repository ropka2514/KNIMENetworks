from nodes.network.util.options_transform import (
    TransformOptions,
    RescaleOptions,
    SymmetrizationOptions,
)
from util.port_objects import (
    NetworkPortObjectSpec,
)

def get_transform_schema(input_schema: NetworkPortObjectSpec, settings) -> NetworkPortObjectSpec:
    """
    Returns the schema for the transformation node based on the provided settings.
    """
    match settings.transform_type:
            case TransformOptions.DISTANCE.name:
                if input_schema.two_mode:
                    raise ValueError("Input must be one-mode.")
                return NetworkPortObjectSpec(
                    source_label=input_schema.source_label,
                    target_label=input_schema.target_label,
                    weight_label="distance",
                    symmetric=input_schema.symmetric,
                    two_mode=False,
                )
            case TransformOptions.REACHABILITY.name:
                if input_schema.two_mode:
                    raise ValueError(
                        "Reachability transform is not supported for two-mode networks."
                    )
                return NetworkPortObjectSpec(
                    source_label=input_schema.source_label,
                    target_label=input_schema.target_label,
                    weight_label="reachable",
                    symmetric=input_schema.symmetric,
                    two_mode=False,
                )
            case TransformOptions.DEPENDENCY.name:
                if input_schema.two_mode:
                    raise ValueError(
                        "Dependency transform is not supported for two-mode networks."
                    )
                return NetworkPortObjectSpec(
                    source_label=input_schema.source_label,
                    target_label=input_schema.target_label,
                    weight_label="dependency",
                    symmetric=input_schema.symmetric,
                    two_mode=False,
                )
            case TransformOptions.MAX_FLOW.name:
                return NetworkPortObjectSpec(
                    source_label=input_schema.source_label,
                    target_label=input_schema.target_label,
                    weight_label="max_flow",
                    symmetric=input_schema.symmetric,
                    two_mode=input_schema.two_mode,
                )
            case TransformOptions.IDENTITY.name:
                return NetworkPortObjectSpec(
                    source_label=input_schema.source_label,
                    target_label=input_schema.target_label,
                    weight_label="identity",
                    symmetric=input_schema.symmetric,
                    two_mode=input_schema.two_mode,
                )
            case TransformOptions.RESCALE.name:
                match settings.rescale_method:
                    case RescaleOptions.GLOBAL_MIN_MAX.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=input_schema.symmetric,
                            two_mode=input_schema.two_mode,
                        )
                    case RescaleOptions.RANDOM_WALK.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=False,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case RescaleOptions.DEGREE_SUM.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=False,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case RescaleOptions.DEGREE_PROD.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=False,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case RescaleOptions.INVERSE.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=input_schema.symmetric,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case RescaleOptions.LOG.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=input_schema.symmetric,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case _:
                        raise ValueError("Invalid rescale method selected.")
            case TransformOptions.SYMMETRY.name:
                match settings.symmetrization_method:
                    case SymmetrizationOptions.SUM.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=True,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case SymmetrizationOptions.AVERAGE.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=True,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case SymmetrizationOptions.MAX.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=True,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case SymmetrizationOptions.MIN.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=True,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case SymmetrizationOptions.BIN_OR.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=True,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case SymmetrizationOptions.BIN_AND.name:
                        return NetworkPortObjectSpec(
                            source_label=input_schema.source_label,
                            target_label=input_schema.target_label,
                            weight_label=input_schema.weight_label,
                            symmetric=True,
                            two_mode=input_schema.two_mode,
                            irreflexive=input_schema.irreflexive,
                        )
                    case _:
                        raise ValueError("Invalid symmetrization method selected.")
            case TransformOptions.FILTER.name:
                return NetworkPortObjectSpec(
                    source_label=input_schema.source_label,
                    target_label=input_schema.target_label,
                    weight_label=input_schema.weight_label,
                    symmetric=input_schema.symmetric,
                    two_mode=input_schema.two_mode,
                    irreflexive=input_schema.irreflexive,
                )
            case _:
                raise ValueError("Invalid transformation type selected.")

