from enum import Enum

ALL_LOGIC_FALLACIES = [
    "Appeal to Emotion",
    "False Causality",
    "Ad Populum",
    "Circular Reasoning",
    "Fallacy of Relevance",
    "Faulty Generalization",
    "Ad Hominem",
    "Fallacy of Extension",
    "Equivocation",
    "Fallacy of Logic",
    "Fallacy of Credibility",
    "Intentional Fallacy",
    "False Dilemma",
]

ALL_LOGIC_FALLACIES_LOWER = [fallacy.lower() for fallacy in ALL_LOGIC_FALLACIES]

ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES = [
    "Fallacy of Relevance",
    "Fallacy of Defective Induction",
    "Fallacy of Presumption",
    "Fallacy of Ambiguity",
]

ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES_LOWER = [fallacy.lower() for fallacy in ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES]

ALL_ARISTOTLE_COARSE_GRAINED_LOGIC_FALLACIES = ["Fallacy of Credibility", "Fallacy of Logic", "Fallacy of Emotion"]

ALL_ARISTOTLE_COARSE_GRAINED_LOGIC_FALLACIES_LOWER = [
    fallacy.lower() for fallacy in ALL_ARISTOTLE_COARSE_GRAINED_LOGIC_FALLACIES
]

ALL_LOGIC_FALLACIES_WITH_DEFINITION = [
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
    "Fallacy of Logic: An error in the logical structure of an argument. ",
    "Intentional Fallacy: Some intentional (sometimes subconscious) action/choice to incorrectly support an argument.",
]

# ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION = [
#     "Fallacy of Relevance: Occurs when premises are logically irrelevant to the conclusion and includes the following subcategories: Ad Hominem, Ad Populum, Appeal to Emotion, Fallacy of Extension, Intentional Fallacy.",
#     "Fallacy of Defective Induction: Premises provide weak or insufficient grounds for the conclusion, often through flawed inductive reasoning and includes the following subcategories: False Causality, False Dilemma, Faulty Generalization, Fallacy of Logic, Fallacy of Credibility.",
#     "Fallacy of Presumption: Relies on unwarranted assumptions, creating unsupported or circular reasoning and includes the following subcategories: Circular Reasoning, Begging the Question, Complex Question, Accident",
#     "Fallacy of Ambiguity: Uses ambiguous language or phrasing that creates confusion or multiple interpretations, disrupting logical connections between premise and conclusion and includes the following subcategories: Equivocation, Amphiboly, Accent, Composition, Division.",
# ]

ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION = [
    "Fallacy of Relevance: These occur when the premises are not logically relevant to the conclusion, often relying on emotional appeals, distractions, or personal attacks rather than valid reasoning.",
    "Fallacy of Defective Induction: These involve weak or insufficient evidence leading to a conclusion, where the premises fail to provide strong support for the argument.",
    "Fallacy of Ambiguity: These arise from unclear or misleading language that creates confusion or misinterpretation, often through ambiguous wording or structure.",
    "Fallacy of Presumption: These occur when an argument assumes something without proper justification, relying on unstated or unsupported premises that fail to validate the conclusion.",
]


ALL_ARISTOTLE_COARSE_GRAINED_FALLACIES_WITH_DEFINITION = [
    "Fallacy of Credibility: These fallacies occur when the appeal to credibility or character is flawed or misused.",
    "Fallacy of Logic: These fallacies occur when the logical structure of an argument is flawed.",
    "Fallacy of Emotion: These fallacies involve manipulative emotional appeals that bypass logical reasoning.",
]


COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS = {
    "Fallacy of Relevance": [
        "ad hominem",
        "ad populum",
        "appeal to emotion",
        "intentional fallacy",
        "fallacy of extension",
        "fallacy of relevance",
    ],
    "Fallacy of Defective Induction": [
        "false causality",
        "false dilemma",
        "faulty generalization",
        "fallacy of logic",
        "fallacy of credibility",
    ],
    "Fallacy of Presumption": ["circular reasoning"],
    "Fallacy of Ambiguity": ["equivocation", "miscellaneous"],
}

COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER = {
    "fallacy of relevance": [
        "ad hominem",
        "ad populum",
        "appeal to emotion",
        "intentional fallacy",
        "fallacy of extension",
        "fallacy of relevance",
    ],
    "fallacy of defective induction": [
        "false causality",
        "false dilemma",
        "faulty generalization",
        "fallacy of logic",
        "fallacy of credibility",
    ],
    "fallacy of presumption": ["circular reasoning"],
    "fallacy of ambiguity": ["equivocation", "miscellaneous"],
}

COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER_WITH_DEFINITIONS = {
    "fallacy of relevance": [
        "ad hominem: The opponent attacks a person instead of arguing against the claims that the person has put forward.",
        "ad populum: A fallacious argument which is based on affirming that something is real or better because the majority thinks so.",
        "appeal to emotion: attempting to arouse non-rational sentiments within the intended audience in order to persuade.",
        "intentional fallacy: Some intentional (sometimes subconscious) action/choice to incorrectly support an argument.",
        "fallacy of extension: An argument that attacks an exaggerated or caricatured version of your opponent’s position.",
        "fallacy of relevance: The argument supporting the claim diverges the attention to issues which are irrelevant for the claim at hand.",
    ],
    "fallacy of defective induction": [
        "false causality: occurs when someone mistakenly assumes that because one event follows another, the first event caused the second, without sufficient evidence for a causal link.",
        "false dilemma: Presenting two alternative options as the only possibilities, when in fact more possibilities exist.",
        "faulty generalization: A generalization is drawn from a sample which is too small, it is not representative of the population or it is not applicable to the situation if all the variables are taken into account.",
        "fallacy of logic:  An error in the logical structure of an argument",
        "fallacy of credibility: happens when someone argues that a claim is true simply because an authority or expert believes it, even if that authority is not a reliable or relevant source on the topic.",
    ],
    "fallacy of presumption": ["circular reasoning: A fallacy where the end of an argument comes back to the beginning without having proven itself."],
    "fallacy of ambiguity": ["equivocation: An argument which uses a key term or phrase in an ambiguous way, with one meaning in one portion of the argument and then another meaning in another portion of the argument.",
                             "miscellaneous"],
}

COPI_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS = {
    value: key
    for key in COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS.keys()
    for value in COPI_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS[key]
}


ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS = {
    "Fallacy of Credibility": [
        "ad hominem",
        "ad populum",
        "fallacy of credibility",
    ],
    "Fallacy of Logic": [
        "false causality",
        "false dilemma",
        "faulty generalization",
        "fallacy of logic",
        "circular reasoning",
        "equivocation",
        "fallacy of relevance",
    ],
    "Fallacy of Emotion": [
        "appeal to emotion",
        "intentional fallacy",
        "fallacy of extension",
    ],
}

ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER = {
    "fallacy of credibility": [
        "ad hominem",
        "ad populum",
        "fallacy of credibility",
    ],
    "fallacy of logic": [
        "false causality",
        "false dilemma",
        "faulty generalization",
        "fallacy of logic",
        "circular reasoning",
        "equivocation",
        "fallacy of relevance",
    ],
    "fallacy of emotion": [
        "appeal to emotion",
        "intentional fallacy",
        "fallacy of extension",
    ],
}

ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS_LOWER_WITH_DEFINITIONS = {
    "fallacy of credibility": [
        "ad hominem: The opponent attacks a person instead of arguing against the claims that the person has put forward.",
        "ad populum: A fallacious argument which is based on affirming that something is real or better because the majority thinks so.",
        "fallacy of credibility: happens when someone argues that a claim is true simply because an authority or expert believes it, even if that authority is not a reliable or relevant source on the topic.",
    ],
    "fallacy of logic": [
        "false causality: occurs when someone mistakenly assumes that because one event follows another, the first event caused the second, without sufficient evidence for a causal link.",
        "false dilemma: Presenting two alternative options as the only possibilities, when in fact more possibilities exist.",
        "faulty generalization: A generalization is drawn from a sample which is too small, it is not representative of the population or it is not applicable to the situation if all the variables are taken into account.",
        "fallacy of logic:  An error in the logical structure of an argument",
        "circular reasoning: A fallacy where the end of an argument comes back to the beginning without having proven itself.",
        "equivocation: An argument which uses a key term or phrase in an ambiguous way, with one meaning in one portion of the argument and then another meaning in another portion of the argument.",
        "fallacy of relevance: The argument supporting the claim diverges the attention to issues which are irrelevant for the claim at hand.",
    ],
    "fallacy of emotion": [
        "appeal to emotion: attempting to arouse non-rational sentiments within the intended audience in order to persuade.",
        "intentional fallacy: Some intentional (sometimes subconscious) action/choice to incorrectly support an argument.",
        "fallacy of extension: An argument that attacks an exaggerated or caricatured version of your opponent’s position.",
    ],
}

ARISTOTLE_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS = {
    value: key
    for key in ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS.keys()
    for value in ARISTOTLE_COARSE_GRAINED_TO_FINE_GRAINDED_MAPPINGS[key]
}


class FallacyClass(Enum):
    FINE_GRAINED = 1
    COPI = 2
    ARISTOTLE = 3


ALL_FALLACIES_PER_FALLACY_CLASS = {
    FallacyClass.FINE_GRAINED: ALL_LOGIC_FALLACIES,
    FallacyClass.COPI: ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES,
    FallacyClass.ARISTOTLE: ALL_ARISTOTLE_COARSE_GRAINED_LOGIC_FALLACIES,
}


ALL_FALLACIES_PER_FALLACY_CLASS_LOWER = {
    FallacyClass.FINE_GRAINED: ALL_LOGIC_FALLACIES_LOWER,
    FallacyClass.COPI: ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES_LOWER,
    FallacyClass.ARISTOTLE: ALL_ARISTOTLE_COARSE_GRAINED_LOGIC_FALLACIES_LOWER,
}
