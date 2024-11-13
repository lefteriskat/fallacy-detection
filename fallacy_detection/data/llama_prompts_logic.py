all_logic_fallacies = [
    "Appeal to Emotion",
    "False Causality",
    "Ad Populum",
    "Circular Reasoning",
    "Fallacy of Relevance",
    "Faulty Generalization",
    "Ad Hominem",
    "Fallacy of Extension",
    "Equivocation",
    "Deductive Fallacy",
    "Fallacy of Credibility",
    "Intentional Fallacy",
    "False Dilemma",
]

all_coarse_grained_fallacies = [
    "Fallacy of Relevance",
    "Fallacy of Defective Induction",
    "Fallacy of Presumption",
    "Fallacy of Ambiguity",
]

all_logic_fallacies_definition = [
    "Appeal To Emotion: attempting to arouse non-rational sentiments within the intended audience in order to persuade.",
    "False Causality: occurs when someone mistakenly assumes that because one event follows another, the first event caused the second, without sufficient evidence for a causal link.",
    "Ad Hominem: The opponent attacks a person instead of arguing against the claims that the person has put forward.",
    "Faulty Generalization: A generalization is drawn from a sample which is too small, it is not representative of the population or it is not applicable to the situation if all the variables are taken into account.",
    "False Dilemma: Presenting two alternative options as the only possibilities, when in fact more possibilities exist. As an the extreme case, tell the audience exactly what actions to take, eliminating any other possible choices (Dictatorship).",
    "Fallacy of Relevance: The argument supporting the claim diverges the attention to issues which are irrelevant for the claim at hand.",
    "Fallacy of Credibility: happens when someone argues that a claim is true simply because an authority or expert believes it, even if that authority is not a reliable or relevant source on the topic.",
    "Ad Populum: A fallacious argument which is based on affirming that something is real or better because the majority thinks so.",
    "Circular Reasoning: A fallacy where the end of an argument comes back to the beginning without having proven itself.",
    "Fallacy of Extension: An argument that attacks an exaggerated or caricatured version of your opponent’s position.",
    "Equivocation: An argument which uses a key term or phrase in an ambiguous way, with one meaning in one portion of the argument and then another meaning in another portion of the argument.",
    "Deductive Fallacy: An error in the logical structure of an argument. ",
    "Intentional Fallacy: Some intentional (sometimes subconscious) action/choice to incorrectly support an argument.",
]

all_coarse_grained_fallacies_definition = [
    "Fallacy of Relevance: Occurs when premises are logically irrelevant to the conclusion and includes the following subcategories: Ad Hominem, Ad Populum, Appeal to Emotion, Fallacy of Extension, Intentional Fallacy.",
    "Fallacy of Defective Induction: Premises provide weak or insufficient grounds for the conclusion, often through flawed inductive reasoning and includes the following subcategories: False Causality, False Dilemma, Faulty Generalization, Fallacy of Logic, Fallacy of Credibility.",
    "Fallacy of Presumption: Relies on unwarranted assumptions, creating unsupported or circular reasoning and includes the following subcategories: Circular Reasoning, Begging the Question, Complex Question, Accident",
    "Fallacy of Ambiguity: Uses ambiguous language or phrasing that creates confusion or multiple interpretations, disrupting logical connections between premise and conclusion and includes the following subcategories: Equivocation, Amphiboly, Accent, Composition, Division.",
]

all_logic_fallacies_definition_prompt_ready = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(all_logic_fallacies_definition)]
)

all_coarse_grained_fallacies_definition_prompt_ready = "\n".join(
    [str(i + 1) + ". " + s for i, s in enumerate(all_coarse_grained_fallacies_definition)]
)

delimiter = "####"

# prompts_targets = [
#         ('''Given the segment below, which of the following fallacies does it have: {fallacies}, or {last_fallacy}?\nSegment: {segment}''', '{fallacy}'),
#         ('''Given the following segment and definitions, determine which of the fallacies defined below occurs in the segment.\nDefinitions:\n{definitions}\n\nSegment: {segment}''', '{fallacy}'),
#         ('Which fallacy does the following segment have: "{segment}"?\n{fallacies}', '{fallacy}')
#     ]

# prompt = """You are a professional logician that needs to determine which of the fallacies defined below occurs in the segment.
#             You must answer only with the fallacy name!
#             So, Given the segment below, which hich of the fallacies defined below occurs in the segment: {fallacies}?\n
#             Segment: {segment}\n
#             Fallacy in the segment: """

# prompt2 = """You are a professional logician that needs to determine which of the fallacies defined below occurs in the segment.
# Given the following segment and definitions, determine which of the fallacies defined below occurs in the segment.
# \nDefinitions:\n{definitions}\n\nSegment: {segment}\n Fallacy in the segment: """

prompt_intro = f"""You will be provided with a text segment and you need to determine which of the fallacy types defined below occurs in this segment. \
The segment will be delimited with {delimiter} characters.
Classify each segment into the fallacy type that you think that occured in the segment.
Provide your output in json format with the \
key: detected_fallacy.
"""

prompt_fallacy_categories = f"""The different fallacy types that may occur in the segment are: {", ".join(fallacy for fallacy in all_logic_fallacies)}."""

prompt_fallacy_definitions = f"""The different fallacy types that may occur in the segment are:
    {all_logic_fallacies_definition_prompt_ready}."""


prompt_fallacy_coarse_categories = f"""The different fallacy types that may occur in the segment are: {", ".join(fallacy for fallacy in all_coarse_grained_fallacies)}."""

prompt_fallacy_coarse_definitions = f"""The different fallacy types that may occur in the segment are:
    {all_coarse_grained_fallacies_definition_prompt_ready}."""

prompt_add_segment = """The segment to be classified is the following: {delimiter}{segment}{delimiter}"""

reminder_prompt = "Don't forget that your response should be in json format with key detected_fallacy, for example detected_fallacy: Fallacy of Relevance"


def get_logic_prompt(coarse_grained: bool = False, include_definitions: bool = False, examples: bool = False):
    if coarse_grained:
        definitions = prompt_fallacy_coarse_definitions
        categories = prompt_fallacy_coarse_categories
    else:
        definitions = prompt_fallacy_definitions
        categories = prompt_fallacy_categories
    if include_definitions:
        return prompt_intro + "\n" + categories + "\nTheir definitions are the following:\n"+ definitions + "\n" +  prompt_add_segment + "\n" + reminder_prompt
    else:
        return prompt_intro + "\n" + categories + "\n" + prompt_add_segment + "\n" + reminder_prompt
