from fallacy_detection.data.definitions import (
    ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES,
    ALL_LOGIC_FALLACIES,
    COPI_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS,
    ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES_LOWER,
    ALL_LOGIC_FALLACIES_LOWER,
)

from fallacy_detection.models.model import TARGET_MODELS

import pandas as pd
import re
import plotly.express as px
from sklearn.metrics import f1_score, accuracy_score


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


def map_to_coarse_grained(fine_grained):
    return COPI_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS.get(fine_grained, "unknown").lower()


OUTPUT_FOLDER = "reports/analysed_results/"
PLOTS_FOLDER = "reports/analysed_results/plots/"
METRICS_FOLDER = "reports/analysed_results/metrics/"


def preprocess_results(dataframe: pd.DataFrame, coarse_grained: bool, from_fine_to_coarse: bool = False):
    # clean predicted_label
    if coarse_grained:
        dataframe["predicted_label"] = dataframe["predicted_label"].map(clean_predicted_coarse_grained_label)
    else:
        dataframe["predicted_label"] = dataframe["predicted_label"].map(clean_predicted_fine_grained_label)

    if from_fine_to_coarse:
        dataframe["predicted_label"] = dataframe["predicted_label"].map(map_to_coarse_grained)
        dataframe["true_label"] = dataframe["true_label"].map(map_to_coarse_grained)

    # create a column that is true if the predicted label is the same as the true label
    dataframe["correct_prediction"] = dataframe["predicted_label"] == dataframe["true_label"]

    return dataframe


def extract_metrics(model_name: str, coarse_grained: bool, definitions: bool, from_fine_to_coarse: bool = False):
    dataframe = pd.read_csv(
        f"reports/{model_name.replace('/', '-')}_{'coarse_grained' if coarse_grained else 'fine_grained'}_results{'_with_definitions' if definitions else '_no_definitions'}.csv"
    )
    dataframe = preprocess_results(dataframe, coarse_grained, from_fine_to_coarse)

    metrics_dict = {"model": model_name.split("/", 1)[1], "definitions": definitions}

    metrics_dict["accuracy"] = (
        accuracy_score(dataframe["true_label"].to_numpy(), dataframe["predicted_label"].to_numpy()) * 100
    )
    metrics_dict["f1 score"] = f1_score(
        dataframe["true_label"].to_numpy(), dataframe["predicted_label"].to_numpy(), average="macro"
    )
    # compute unknown percentage
    unknown_count = dataframe["predicted_label"].eq("unknown").sum()
    total_count = len(dataframe["predicted_label"])
    unknown_percentage = (unknown_count / total_count) * 100
    metrics_dict["failed"] = unknown_percentage
    # compute percentage of labels not found in the LOGIC's dataset classes
    if coarse_grained or from_fine_to_coarse:
        different_labels_count = (
            dataframe["predicted_label"]
            .str.lower()
            .apply(lambda x: x not in ALL_COPI_COARSE_GRAINED_LOGIC_FALLACIES_LOWER and x != "unknown")
            .sum()
        )
    else:
        different_labels_count = (
            dataframe["predicted_label"]
            .str.lower()
            .apply(lambda x: x not in ALL_LOGIC_FALLACIES_LOWER and x != "unknown")
            .sum()
        )
    different_labels_percentage = (different_labels_count / total_count) * 100
    metrics_dict["unknown labels"] = different_labels_percentage
    return metrics_dict


def create_plots(model_name: str, coarse_grained: bool, definitions: bool, from_fine_to_coarse: bool = False):
    dataframe = pd.read_csv(
        f"reports/{model_name.replace('/', '-')}_{'coarse_grained' if coarse_grained else 'fine_grained'}_results{'_with_definitions' if definitions else '_no_definitions'}.csv"
    )
    dataframe = preprocess_results(dataframe, coarse_grained, from_fine_to_coarse)

    filename1 = f"{PLOTS_FOLDER}true_label_hist_{model_name.replace('/', '-')}_{'coarse_grained' if coarse_grained else 'fine_grained'}_results{'_with_definitions' if definitions else '_no_definitions'}.png"
    filename2 = f"{PLOTS_FOLDER}predicted_label_hist_{model_name.replace('/', '-')}_{'coarse_grained' if coarse_grained else 'fine_grained'}_results{'_with_definitions' if definitions else '_no_definitions'}.png"

    if from_fine_to_coarse:
        title1 = "Results when mapping fine grained results to coarse grained classes"
        title2 = "Results when mapping fine grained results to coarse grained classes"
    else:
        title1 = (
            f"Coarse Grained Classes {'with defintions' if definitions else 'without defintions'} True labels Histogram"
            if coarse_grained
            else f"Fine Grained Classes {'with defintions' if definitions else 'without defintions'} True labels Histogram"
        )
        title2 = (
            f"Coarse Grained Classes {'with defintions' if definitions else 'without defintions'} Predicted labels Histogram"
            if coarse_grained
            else f"Fine Grained Classes {'with defintions' if definitions else 'without defintions'} Predicted labels Histogram"
        )

    fig1 = px.histogram(dataframe, x="true_label", color="correct_prediction", text_auto=True, title=title1)
    fig2 = px.histogram(dataframe, x="predicted_label", color="correct_prediction", text_auto=True, title=title2)

    fig1.write_image(filename1)
    fig2.write_image(filename2)


def run_metrics(coarse_grained: bool = False, from_fine_to_coarse: bool = False):
    results_data = []
    for model in TARGET_MODELS:
        results_data.append(
            extract_metrics(model, coarse_grained, definitions=False, from_fine_to_coarse=from_fine_to_coarse)
        )
        results_data.append(
            extract_metrics(model, coarse_grained, definitions=True, from_fine_to_coarse=from_fine_to_coarse)
        )

    df = pd.DataFrame(results_data)
    # Round all float columns to 3 decimal places
    for col in df.select_dtypes(include=["float"]).columns:
        df[col] = df[col].apply(lambda x: f"{x:.3f}")

    if from_fine_to_coarse:
        caption = "Results when mapping fine grained results to coarse grained classes"
    else:
        caption = "Coarse Grained Classes Results" if coarse_grained else "Fine Grained Classes Results"
    print(df.to_latex(index=False, caption=caption))


def run_plots(from_fine_to_coarse: bool = False):
    for model in TARGET_MODELS:
        create_plots(model, coarse_grained=False, definitions=False)
        create_plots(model, coarse_grained=False, definitions=True)
        create_plots(model, coarse_grained=True, definitions=False)
        create_plots(model, coarse_grained=True, definitions=True)


if __name__ == "__main__":
    run_metrics(coarse_grained=False)
    run_metrics(coarse_grained=True)
    run_metrics(from_fine_to_coarse=True)

    run_plots()
