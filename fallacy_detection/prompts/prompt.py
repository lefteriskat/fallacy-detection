from fallacy_detection.data.definitions import (
    ALL_LOGIC_FALLACIES,
    ALL_LOGIC_FALLACIES_WITH_DEFINITION,
    ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES,
    ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION,
    ALL_ARISTOTLE_COARSE_GRAINED_LOGIC_FALLACIES,
    ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_WITH_DEFINITION,
    FallacyClass,
)


ALL_LOGIC_FALLACIES_PROMPT_READY = "\n".join([str(i + 1) + ". " + s for i, s in enumerate(ALL_LOGIC_FALLACIES)])

ALL_LOGIC_FALLACIES_WITH_DEFINITION_PROMPT_READY = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(ALL_LOGIC_FALLACIES_WITH_DEFINITION)]
)


ALL_COPI_COARSE_GRAINED_FALLACIES_PROMPT_READY = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES)]
)
ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION_PROMPT_READY = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION)]
)

ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_PROMPT_READY = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(ALL_ARISTOTLE_COARSE_GRAINED_LOGIC_FALLACIES)]
)
ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_WITH_DEFINITION_PROMPT_READY = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_WITH_DEFINITION)]
)


DELIMITER = "####"

# PROMPT1_INTRO = f"""You will be provided with a text segment and you need to determine which of the fallacy types defined below occurs in this segment.\n\
# The segment will be delimited with {DELIMETER} characters.\nClassify each segment into the fallacy type that you think that occured in the segment.\n
# Provide your output in json format with the key: detected_fallacy.
# """

PROMPT1_INTRO =f"""You will be provided with a text segment, delimited by {DELIMITER} characters, and your task is to classify it into one of the fallacy types listed below.\n\
Provide your output in JSON format with the key: `detected_fallacy`. The value should be the name of the detected fallacy, chosen from the list below. Do not include any explanation or commentary.\n\
The {DELIMITER} characters are only delimiters for the segment. Do not include them in your classification or output."""

PROMPT1_FALLACY_CLASSES = (
    f"""The possible fallacy types are:\n{ALL_LOGIC_FALLACIES_PROMPT_READY}\n"""
)

PROMPT1_FALLACY_CLASSES_WITH_DEFINITION = f"""The possible fallacy types are:\n\
{ALL_LOGIC_FALLACIES_WITH_DEFINITION_PROMPT_READY}."""


PROMPT1_COPI_COARSE_GRAINED_FALLACY_CLASSES = f"""The possible fallacy types are:\n\
{ALL_COPI_COARSE_GRAINED_FALLACIES_PROMPT_READY}."""

PROMPT1_COPI_COARSE_GRAINED_FALLACY_CLASSES_WITH_DEFINITION = f"""The possible fallacy types are:\n\
{ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION_PROMPT_READY}."""

PROMPT1_ARISTOTLE_COARSE_GRAINED_FALLACY_CLASSES = f"""The possible fallacy types are:\n\
{ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_PROMPT_READY}."""

PROMPT1_ARISTOTLE_COARSE_GRAINED_FALLACY_CLASSES_WITH_DEFINITION = f"""The possible fallacy types are:\n\
{ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_WITH_DEFINITION_PROMPT_READY}."""

PROMPT1_ADD_SEGMENT = """The segment to be classified is the following: {delimiter}{segment}{delimiter}"""

REMINDER_PROMPT1 = """\n\nProvide your output in strict JSON format with the key `detected_fallacy`. For example:
{
  "detected_fallacy": "name_of_fallacy"
}"""


SYSTEM_PROMPT = """You are a knowledgable expert in analysing fallacies in discourses. 
Please ensure that your responses are socially unbiased in nature.
Your response should not be lengthy.
Answer the last question."""

DEFINITION_PROMPT = """Based on the following definitions of fallacies:\n\
{fallacies}\n\
Given a segment of discourse below, determine which of the fallacies defined above is present in the argument?
Segment:\n{segment}"""


NO_DEFINITION_PROMPT = """Given the following types of fallacies:\n\
{fallacies}\n\
Given the segment of discourse below, determine which of the fallacies given is present in the argument.
Segment:\n{segment}"""

REMINDER_PROMPT2 = """\n\nRespond strictly in JSON format. For example:
{
  "detected_fallacy": "name_of_fallacy"
}

Do not include any explanation or additional commentary."""

def get_logic_prompt(
    option: int,
    fallacy_class: FallacyClass = FallacyClass.FINE_GRAINED,
    include_definitions: bool = False,
    segment : str = "{segment}",
    cot: bool = False,
    few_shot: bool = False,
):
    if option == 1:
        if fallacy_class == FallacyClass.FINE_GRAINED:
            definitions = PROMPT1_FALLACY_CLASSES_WITH_DEFINITION
            classes = PROMPT1_FALLACY_CLASSES
        elif fallacy_class == FallacyClass.COPI:
            definitions = PROMPT1_COPI_COARSE_GRAINED_FALLACY_CLASSES_WITH_DEFINITION
            classes = PROMPT1_COPI_COARSE_GRAINED_FALLACY_CLASSES
        elif fallacy_class == FallacyClass.ARISTOTLE:
            definitions = PROMPT1_ARISTOTLE_COARSE_GRAINED_FALLACY_CLASSES_WITH_DEFINITION
            classes = PROMPT1_ARISTOTLE_COARSE_GRAINED_FALLACY_CLASSES
        else:
            raise NotImplementedError
        if include_definitions:
            return PROMPT1_INTRO + "\n" + definitions + "\n" + PROMPT1_ADD_SEGMENT.format(delimiter=DELIMITER, segment=segment) + "\n" + REMINDER_PROMPT1
        else:
            return PROMPT1_INTRO + "\n" + classes + "\n" + PROMPT1_ADD_SEGMENT.format(delimiter=DELIMITER, segment=segment) + "\n" + REMINDER_PROMPT1
    elif option == 2:
        if fallacy_class == FallacyClass.FINE_GRAINED:
            prompt_2_definitions = ALL_LOGIC_FALLACIES_WITH_DEFINITION_PROMPT_READY
            prompt_2_no_definitions = ALL_LOGIC_FALLACIES_PROMPT_READY
        elif fallacy_class == FallacyClass.COPI:
            prompt_2_definitions = ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION_PROMPT_READY
            prompt_2_no_definitions = ALL_COPI_COARSE_GRAINED_FALLACIES_PROMPT_READY
        elif fallacy_class == FallacyClass.ARISTOTLE:
            prompt_2_definitions = ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_WITH_DEFINITION_PROMPT_READY
            prompt_2_no_definitions = ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_PROMPT_READY
        else:
            raise NotImplementedError

        if include_definitions:
            return SYSTEM_PROMPT + "\n" + DEFINITION_PROMPT.format(fallacies=prompt_2_definitions, segment=segment) + REMINDER_PROMPT2
        else:
            return (
                SYSTEM_PROMPT
                + "\n"
                + NO_DEFINITION_PROMPT.format(fallacies=prompt_2_no_definitions, segment=segment)
                + REMINDER_PROMPT2
            )


def main():
    for option in [1, 2]:
        print(get_logic_prompt(option=option, fallacy_class=FallacyClass.FINE_GRAINED, include_definitions=True))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(get_logic_prompt(option=option, fallacy_class=FallacyClass.COPI, include_definitions=True))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(get_logic_prompt(option=option, fallacy_class=FallacyClass.ARISTOTLE, include_definitions=True))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


if __name__ == "__main__":
    main()