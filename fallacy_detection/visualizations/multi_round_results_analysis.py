from fallacy_detection.data.definitions import (
    COPI_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS,
    ARISTOTLE_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS,
    ALL_FALLACIES_PER_FALLACY_CLASS,
    ALL_FALLACIES_PER_FALLACY_CLASS_LOWER,
    FallacyClass,
)

from fallacy_detection.models.model import TARGET_MODELS

import pandas as pd
import re
import plotly.express as px
from sklearn.metrics import f1_score, accuracy_score

FAILED = "failed"


def clean_predicted_label(json_label, fallacy_class: FallacyClass):
    # Use regular expressions to find the JSON part of the string
    for fallacy in ALL_FALLACIES_PER_FALLACY_CLASS[fallacy_class]:
        try:
            if fallacy.lower() in json_label.lower():
                return fallacy.lower()
        except:
            return FAILED

    fallacy_match = re.search(r'"detected_fallacy"\s*:\s*"([^"]+)"', json_label)
    if fallacy_match:
        # Extract the matched fallacy if found
        return fallacy_match.group(1)
    else:
        return FAILED


def map_to_coarse_grained(fine_grained, fallacy_class: FallacyClass):
    if fallacy_class == FallacyClass.COPI:
        return COPI_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS.get(fine_grained, FAILED).lower()
    elif fallacy_class == FallacyClass.ARISTOTLE:
        return ARISTOTLE_FINE_GRAINED_TO_COARSE_GRAINDED_MAPPINGS.get(fine_grained, FAILED).lower()


OUTPUT_FOLDER = "reports/analysed_results/"
PLOTS_FOLDER = "reports/analysed_results/plots/"
METRICS_FOLDER = "reports/analysed_results/metrics/"


def preprocess_results(dataframe: pd.DataFrame, fallacy_class: FallacyClass, from_fine_to_coarse: FallacyClass):
    # clean predicted_label

    dataframe["round1_predicted_label"] = dataframe["round1_predicted_label"].apply(
        lambda predicted_label: clean_predicted_label(predicted_label, fallacy_class)
    )

    dataframe["round1_true_label"] = dataframe["round1_true_label"].apply(lambda x: x.lower())
    dataframe["true_label"] = dataframe["true_label"].apply(lambda x: x.lower())

    # create a column that is true if the predicted label is the same as the true label
    dataframe["round1_correct_prediction"] = dataframe["round1_predicted_label"] == dataframe["round1_true_label"]

    dataframe["predicted_label"] = dataframe["predicted_label"].apply(
        lambda predicted_label: clean_predicted_label(predicted_label, FallacyClass.FINE_GRAINED)
    )

    # create a column that is true if the predicted label is the same as the true label
    dataframe["correct_prediction"] = dataframe["predicted_label"] == dataframe["true_label"]

    return dataframe


def extract_metrics(
    model_name: str,
    prompt_option: int,
    fallacy_class: FallacyClass,
    definitions: bool,
    from_fine_to_coarse: FallacyClass = FallacyClass.FINE_GRAINED,
):
    filename = f"final_reports_mr/{model_name.replace('/', '-')}_prompt{prompt_option}_no_cot_{fallacy_class.name}_results{'_with_definitions' if definitions else '_no_definitions'}_1995_temp1.0.csv"
    dataframe = pd.read_csv(filename)
    dataframe = preprocess_results(dataframe, fallacy_class, from_fine_to_coarse)

    metrics_dict = {"model": model_name.split("/", 1)[1], "definitions": definitions, "prompt": prompt_option}

    metrics_dict["round1_accuracy"] = (
        accuracy_score(dataframe["round1_true_label"].to_numpy(), dataframe["round1_predicted_label"].to_numpy()) * 100
    )
    metrics_dict["round1_f1 score"] = f1_score(
        dataframe["round1_true_label"].to_numpy(), dataframe["round1_predicted_label"].to_numpy(), average="macro"
    )

    metrics_dict["accuracy"] = (
        accuracy_score(dataframe["true_label"].to_numpy(), dataframe["predicted_label"].to_numpy()) * 100
    )
    metrics_dict["f1 score"] = f1_score(
        dataframe["true_label"].to_numpy(), dataframe["predicted_label"].to_numpy(), average="macro"
    )
    # compute unknown percentage
    unknown_count = dataframe["predicted_label"].eq(FAILED).sum()
    total_count = len(dataframe["predicted_label"])
    unknown_percentage = (unknown_count / total_count) * 100
    metrics_dict["failed"] = unknown_percentage
    # compute percentage of labels not found in the LOGIC's dataset classes
    different_labels_count = (
        dataframe["predicted_label"]
        .str.lower()
        .apply(lambda x: x not in ALL_FALLACIES_PER_FALLACY_CLASS_LOWER[FallacyClass.FINE_GRAINED] and x != FAILED)
        .sum()
    )
    different_labels_percentage = (different_labels_count / total_count) * 100
    metrics_dict["unknown labels"] = different_labels_percentage
    return metrics_dict


def create_plots(model_name: str, coarse_grained: bool, definitions: bool, from_fine_to_coarse: bool = False):
    filename = f"reports/{model_name.replace('/', '-')}_{'coarse_grained' if coarse_grained else 'fine_grained'}_results{'_with_definitions' if definitions else '_no_definitions'}.csv"
    dataframe = pd.read_csv(filename)
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


def run_metrics(fallacy_class: FallacyClass, from_fine_to_coarse: FallacyClass = FallacyClass.FINE_GRAINED):
    results_data = []
    PROMPT_OPTIONS = [1, 2]
    for prompt_option in PROMPT_OPTIONS:
        for model in TARGET_MODELS:
            results_data.append(
                extract_metrics(
                    model, prompt_option, fallacy_class, definitions=False, from_fine_to_coarse=from_fine_to_coarse
                )
            )
            results_data.append(
                extract_metrics(
                    model, prompt_option, fallacy_class, definitions=True, from_fine_to_coarse=from_fine_to_coarse
                )
            )

    df = pd.DataFrame(results_data)
    # Round all float columns to 3 decimal places
    for col in df.select_dtypes(include=["float"]).columns:
        df[col] = df[col].apply(lambda x: f"{x:.3f}")

    if from_fine_to_coarse != FallacyClass.FINE_GRAINED:
        caption = "Results when mapping fine grained results to coarse grained classes"
    else:
        caption = f"{fallacy_class.name} Classes Results"
    print(df.to_latex(index=False, caption=caption))


def run_plots(from_fine_to_coarse: bool = False):
    for model in TARGET_MODELS:
        create_plots(model, coarse_grained=False, definitions=False)
        create_plots(model, coarse_grained=False, definitions=True)
        create_plots(model, coarse_grained=True, definitions=False)
        create_plots(model, coarse_grained=True, definitions=True)


if __name__ == "__main__":
    # run_metrics(fallacy_class=FallacyClass.FINE_GRAINED)
    run_metrics(fallacy_class=FallacyClass.COPI)
    run_metrics(fallacy_class=FallacyClass.ARISTOTLE)
    # run_metrics(fallacy_class=FallacyClass.FINE_GRAINED, from_fine_to_coarse=FallacyClass.COPI)
    # run_metrics(fallacy_class=FallacyClass.FINE_GRAINED, from_fine_to_coarse=FallacyClass.ARISTOTLE)

    # run_plots()
