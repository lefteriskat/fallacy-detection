from fallacy_detection.data.definitions import (
    ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER,
    COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER,
    COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER_WITH_DEFINITIONS,
    ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER_WITH_DEFINITIONS,
    ALL_FALLACIES_PER_FALLACY_CLASS,
    FallacyClass,
)
import re

FAILED = "failed"


def clean_predicted_label(json_label, fallacy_class: FallacyClass):
    # Use regular expressions to find the JSON part of the string
    for fallacy in ALL_FALLACIES_PER_FALLACY_CLASS[fallacy_class]:
        try:
            if fallacy.lower() in json_label:
                return fallacy
        except:
            return FAILED

    fallacy_match = re.search(r'"detected_fallacy"\s*:\s*"([^"]+)"', json_label)
    if fallacy_match:
        # Extract the matched fallacy if found
        return fallacy_match.group(1)
    else:
        return FAILED


def get_fine_grained_from_coarse_grained(
    fallacy_class: FallacyClass, fallacy: str, include_definitions: bool
) -> list[str]:
    if fallacy_class == FallacyClass.COPI and not include_definitions:
        return COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER.get(fallacy, None)
    elif fallacy_class == FallacyClass.COPI and include_definitions:
        return COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER_WITH_DEFINITIONS.get(fallacy, None)
    elif fallacy_class == FallacyClass.ARISTOTLE and not include_definitions:
        return ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER.get(fallacy, None)
    elif fallacy_class == FallacyClass.ARISTOTLE and include_definitions:
        return ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER_WITH_DEFINITIONS.get(fallacy, None)
    return None
