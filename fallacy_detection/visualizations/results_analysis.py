from fallacy_detection.data.definitions import (
    ALL_COPI_COARSE_GRAINED_FALLACIES_WITH_DEFINITION,
    ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES,
    ALL_LOGIC_FALLACIES,
    ALL_LOGIC_FALLACIES_WITH_DEFINITION,
)

from fallacy_detection.models.model import TARGET_MODELS

import pandas as pd
import json
import re
import plotly.express as px


def clean_predicted_coarse_grained_label(json_label):
    # Use regular expressions to find the JSON part of the string
    for coarse_grained_fallacy in ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES:
        if coarse_grained_fallacy.lower() in json_label:
            return coarse_grained_fallacy.lower()
    
    fallacy_match = re.search(r'"detected_fallacy"\s*:\s*"([^"]+)"', json_label)
    if fallacy_match:
        # Extract the matched fallacy if found
        return fallacy_match.group(1) if fallacy_match else json_label
    else:
        return "unknown"


def clean_predicted_fine_grained_label(json_label):
    # Use regular expressions to find the JSON part of the string
    for coarse_grained_fallacy in ALL_LOGIC_FALLACIES:
        if coarse_grained_fallacy.lower() in json_label:
            return coarse_grained_fallacy.lower()
    
    fallacy_match = re.search(r'"detected_fallacy"\s*:\s*"([^"]+)"', json_label)
    if fallacy_match:
        # Extract the matched fallacy if found
        return fallacy_match.group(1) if fallacy_match else json_label
    else:
        return "unknown"


dataframe = pd.read_csv("../reports/mistralai-Mistral-7B-Instruct-v0.3_fine_grained_results_no_definitions.csv")

#clean predicted_label
dataframe["predicted_label"] = dataframe["predicted_label"].map(clean_predicted_fine_grained_label)




def extract_metrics(model_name: str):
    pass

def create_plots(model_name: str):
    