from omegaconf import DictConfig, OmegaConf
import hydra
import pandas as pd
from tqdm import tqdm

from fallacy_detection.data.logic_dataset import LogicDataset
from fallacy_detection.utils.settings import Settings
from fallacy_detection.data.definitions import FallacyClass
from torch.utils.data import DataLoader
from fallacy_detection.utils.logging_config import setup_logger
import torch
from accelerate import Accelerator

logger = setup_logger()


@hydra.main(version_base=None, config_path="../config", config_name="config")
def run_multiple_round(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    settings = Settings(cfg)
    Settings.set_seed()
    accelerator = Accelerator()
    device = accelerator.device
    print(device)
    my_pipeline = settings.get_pipeline_from_hf()

    logic_dataset = LogicDataset(cfg)

    fallacy_class = FallacyClass(cfg.prompt.fallacy_classes)
    prompt_option = cfg.prompt.option
    cot = cfg.prompt.cot

    # Create the DataLoader
    batch_size = 1  # Set batch size as needed
    dataloader = DataLoader(logic_dataset, batch_size=batch_size, shuffle=False)
    total = 0
    correct = 0
    predicted_round1_labels = []
    true_round1_labels = []
    predicted_labels = []
    true_labels = []
    original_texts = []
    output_file = f"reports_mr2/{str(cfg.model.name).replace('/', '-')}_prompt{prompt_option}_{'basic_cot' if cot else 'no_cot'}_{fallacy_class.name}_results{'_with_definitions' if cfg.prompt.definitions else '_no_definitions'}.csv"
    logger.info(f"Starting experiment with output file:\n{output_file}")
    for batch in tqdm(dataloader):
        text_segments = batch["text"]
        fine_grained_fallacy_labels = batch["fallacy_type"]
        copi_coarse_labels = batch["copi_fallacy_type"]
        aristotle_coarse_labels = batch["aristotle_fallacy_type"]
        with torch.no_grad():
            for round in [1, 2]:
                if round == 1:
                    messages = settings.get_messages(text_segments)
                    # messages.to(device)
                    outputs = my_pipeline(
                        messages,
                        max_new_tokens=256,
                    )

                    if fallacy_class == FallacyClass.FINE_GRAINED:
                        target_round1_label = fine_grained_fallacy_labels[0].lower()
                    elif fallacy_class == FallacyClass.COPI:
                        target_round1_label = copi_coarse_labels[0].lower()
                    elif fallacy_class == FallacyClass.ARISTOTLE:
                        target_round1_label = aristotle_coarse_labels[0].lower()
                    else:
                        raise NotImplementedError

                    predicted_round1_label = outputs[0][0]["generated_text"][-1]["content"]
                    if total % 10 == 0:
                        logger.info(f"Round 1 Generated Text:{outputs[0][0]['generated_text']}")
                        logger.info(f"Round 1 Predicted_label:{predicted_round1_label}")
                        logger.info(f"Round 1 True Label:{target_round1_label}")

                    predicted_round1_labels.append(predicted_round1_label.lower())
                    true_round1_labels.append(target_round1_label)
                elif round == 2:
                    messages = settings.get_messages(text_segments, outputs[0][0]["generated_text"])
                    outputs = my_pipeline(
                        messages,
                        max_new_tokens=256,
                    )

                    target_label = fine_grained_fallacy_labels[0].lower()
                    if total % 10 == 0:
                        logger.info(f"Round 2 Generated Text:{outputs[0][0]['generated_text']}")
                        logger.info(f"Round 2 Predicted_label:{outputs[0][0]['generated_text'][-1]}")
                        logger.info(f"Round 2 True Label:{target_label}")

                    predicted = outputs[0][0]["generated_text"][-1]["content"]
                    total += 1
                    if target_label in predicted.lower():
                        correct += 1
                    predicted_labels.append(predicted.lower())
                    true_labels.append(target_label)
                    original_texts.append(text_segments[0])

    logger.info(f"accuracy = {correct/total}")
    results_df = pd.DataFrame(
        {
            "text": original_texts,
            "round1_true_label": true_round1_labels,
            "round1_predicted_label": predicted_round1_labels,
            "true_label": true_labels,
            "predicted_label": predicted_labels,
        }
    )
    results_df.to_csv(output_file)
    logger.info(f"Finished experiment with output file:\n{output_file}")


if __name__ == "__main__":
    run_multiple_round()
