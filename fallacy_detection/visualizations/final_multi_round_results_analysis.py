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
import numpy as np
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
    
    dataframe["round1_true_label"] = dataframe["round1_true_label"].apply(lambda x : x.lower())
    dataframe["true_label"] = dataframe["true_label"].apply(lambda x : x.lower())

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
    metrics_dict = {"model": model_name.split("/", 1)[1], "definitions": definitions, "prompt": prompt_option,
                    "round1_accuracy":[], "round1_f1 score":[],
                    "accuracy":[], "f1 score": [], "failed": [], "unknown labels":[]}

    for seed in [42, 64, 128, 256, 1995, 2025, 2055]:
        filename = f"final_reports_mr/{model_name.replace('/', '-')}_prompt{prompt_option}_no_cot_{fallacy_class.name}_results{'_with_definitions' if definitions else '_no_definitions'}_{seed}_temp1.0.csv"
        dataframe = pd.read_csv(filename)
        dataframe = preprocess_results(dataframe, fallacy_class, from_fine_to_coarse)
        
        metrics_dict["round1_accuracy"] += [
            accuracy_score(dataframe["round1_true_label"].to_numpy(), dataframe["round1_predicted_label"].to_numpy()) * 100
        ]
        metrics_dict["round1_f1 score"] += [f1_score(
            dataframe["round1_true_label"].to_numpy(), dataframe["round1_predicted_label"].to_numpy(), average="macro"
        ) * 100]
        
        metrics_dict["accuracy"] += [
            accuracy_score(dataframe["true_label"].to_numpy(), dataframe["predicted_label"].to_numpy()) * 100
        ]
        metrics_dict["f1 score"] += [f1_score(
            dataframe["true_label"].to_numpy(), dataframe["predicted_label"].to_numpy(), average="macro"
        )*100]
        # compute unknown percentage
        unknown_count = dataframe["predicted_label"].eq(FAILED).sum()
        total_count = len(dataframe["predicted_label"])
        unknown_percentage = (unknown_count / total_count) * 100
        metrics_dict["failed"] += [unknown_percentage]
        # compute percentage of labels not found in the LOGIC's dataset classes
        different_labels_count = (
            dataframe["predicted_label"]
            .str.lower()
            .apply(
                lambda x: x
                not in ALL_FALLACIES_PER_FALLACY_CLASS_LOWER[
                    FallacyClass.FINE_GRAINED
                ]
                and x != FAILED
            )
            .sum()
        )
        different_labels_percentage = (different_labels_count / total_count) * 100
        metrics_dict["unknown labels"] += [different_labels_percentage]
        
    r1accuracy_mean = round(float(np.mean(metrics_dict["round1_accuracy"])),3)
    r1accuracy_std = round(float(np.std(metrics_dict["round1_accuracy"])),3)
    metrics_dict["round1_accuracy"] = (r1accuracy_mean, r1accuracy_std)
    r1f1_score_mean = round(float(np.mean(metrics_dict["round1_f1 score"])),3)
    r1f1_score_std = round(float(np.std(metrics_dict["round1_f1 score"])),3)
    metrics_dict["round1_f1 score"] = (r1f1_score_mean, r1f1_score_std)
    accuracy_mean = round(float(np.mean(metrics_dict["accuracy"])),3)
    accuracy_std = round(float(np.std(metrics_dict["accuracy"])),3)
    metrics_dict["accuracy"] = (accuracy_mean, accuracy_std)
    f1_score_mean = round(float(np.mean(metrics_dict["f1 score"])),3)
    f1_score_std = round(float(np.std(metrics_dict["f1 score"])),3)
    metrics_dict["f1 score"] = (f1_score_mean, f1_score_std)
    failed_mean = round(float(np.mean(metrics_dict["failed"])),3)
    failed_std = round(float(np.std(metrics_dict["failed"])),3)
    metrics_dict["failed"] = (failed_mean, failed_std)
    unknown_labels_mean = round(float(np.mean(metrics_dict["unknown labels"])),3)
    unknown_labels_std = round(float(np.std(metrics_dict["unknown labels"])),3)
    metrics_dict["unknown labels"] = (unknown_labels_mean, unknown_labels_std)
    return metrics_dict


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


if __name__ == "__main__":
    #run_metrics(fallacy_class=FallacyClass.FINE_GRAINED)
    run_metrics(fallacy_class=FallacyClass.COPI)
    run_metrics(fallacy_class=FallacyClass.ARISTOTLE)
    #run_metrics(fallacy_class=FallacyClass.FINE_GRAINED, from_fine_to_coarse=FallacyClass.COPI)
    #run_metrics(fallacy_class=FallacyClass.FINE_GRAINED, from_fine_to_coarse=FallacyClass.ARISTOTLE)

    # run_plots()
