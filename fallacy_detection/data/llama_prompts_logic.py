from fallacy_detection.data.definitions import (
    ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES,
    ALL_LOGIC_FALLACIES,
    ALL_LOGIC_FALLACIES_WITH_DEFINITION,
    ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION,
)

all_logic_fallacies_definition_prompt_ready = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(ALL_LOGIC_FALLACIES_WITH_DEFINITION)]
)

all_coarse_grained_fallacies_definition_prompt_ready = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION)]
)

delimiter = "####"

prompt_intro = f"""You will be provided with a text segment and you need to determine which of the fallacy types defined below occurs in this segment. \
The segment will be delimited with {delimiter} characters.
Classify each segment into the fallacy type that you think that occured in the segment.
Provide your output in json format with the \
key: detected_fallacy.
"""

prompt_fallacy_categories = f"""The different fallacy types that may occur in the segment are: {chr(10).join([str(i + 1) + '. ' + s for i, s in enumerate(ALL_LOGIC_FALLACIES)])}."""

prompt_fallacy_definitions = f"""The different fallacy types that may occur in the segment are:
    {all_logic_fallacies_definition_prompt_ready}."""


prompt_fallacy_coarse_categories = f"""The different fallacy types that may occur in the segment are: {chr(10).join([str(i + 1) + '. ' + s for i, s in enumerate(ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES)])}."""

prompt_fallacy_coarse_definitions = f"""The different fallacy types that may occur in the segment are:
    {all_coarse_grained_fallacies_definition_prompt_ready}."""

prompt_add_segment = """The segment to be classified is the following: {delimiter}{segment}{delimiter}"""

reminder_prompt = "Respond with only the label from the list above. Do not include any explanation, additional commentary, or reasoning.\
                   Your response should be in in json format with key detected_fallacy, for example detected_fallacy: Fallacy of Relevance"


def get_logic_prompt(coarse_grained: bool = False, include_definitions: bool = False, examples: bool = False):
    if coarse_grained:
        definitions = prompt_fallacy_coarse_definitions
        categories = prompt_fallacy_coarse_categories
    else:
        definitions = prompt_fallacy_definitions
        categories = prompt_fallacy_categories
    if include_definitions:
        return (
            prompt_intro
            + "\n"
            + categories
            + "\nTheir definitions are the following:\n"
            + definitions
            + "\n"
            + reminder_prompt
            + "\n"
            + prompt_add_segment
        )
    else:
        return prompt_intro + "\n" + categories + "\n" + reminder_prompt + "\n" + prompt_add_segment
