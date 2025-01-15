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
def run_zero_shot(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    settings = Settings(cfg)
    Settings.set_seed(42)
    accelerator = Accelerator()
    device = accelerator.device
    print(device)
    tokenizer = settings.get_tokenizer_from_hf()
    model = settings.get_model_from_hf()
    model.generation_config.pad_token_id = tokenizer.pad_token_id

    logic_dataset = LogicDataset(cfg)

    fallacy_class = FallacyClass(cfg.prompt.fallacy_classes)
    prompt_option = cfg.prompt.option
    cot = cfg.prompt.cot

    model.eval()
    # Create the DataLoader
    batch_size = 1  # Set batch size as needed
    dataloader = DataLoader(logic_dataset, batch_size=batch_size, shuffle=False)
    total = 0
    correct = 0
    predicted_labels = []
    true_labels = []
    original_texts = []
    output_file = f"final_reports/{str(cfg.model.name).replace('/', '-')}_prompt{prompt_option}_{'basic_cot' if cot else 'no_cot'}_{fallacy_class.name}_results{'_with_definitions' if cfg.prompt.definitions else '_no_definitions'}.csv"
    logger.info(f"Starting experiment with output file:\n{output_file}")
    for batch in tqdm(dataloader):
        text_segments = batch["text"]
        fine_grained_fallacy_labels = batch["fallacy_type"]
        copi_coarse_labels = batch["copi_fallacy_type"]
        aristotle_coarse_labels = batch["aristotle_fallacy_type"]
        with torch.no_grad():
            inputs = settings.get_model_inputs(tokenizer, text_segments, device)

            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
            )

            # Decode and print output
            for i in range(len(outputs)):
                prompt_length = inputs["input_ids"][0].shape[0]
                predicted_all = tokenizer.decode(
                    outputs[i], skip_special_tokens=True, clean_up_tokenization_spaces=True
                )
                predicted = tokenizer.decode(
                    outputs[i][prompt_length:], skip_special_tokens=True, clean_up_tokenization_spaces=True
                )

                if fallacy_class == FallacyClass.FINE_GRAINED:
                    target_label = fine_grained_fallacy_labels[i].lower()
                elif fallacy_class == FallacyClass.COPI:
                    target_label = copi_coarse_labels[i].lower()
                elif fallacy_class == FallacyClass.ARISTOTLE:
                    target_label = aristotle_coarse_labels[i].lower()
                else:
                    raise NotImplementedError

                if total % 10 == 0:
                    logger.info(f"Generated Text:{predicted_all}")
                    logger.info(f"Predicted_label:{predicted}")
                    logger.info(f"True Label:{target_label}")
                total += 1

                if target_label in predicted.lower():
                    correct += 1
                predicted_labels.append(predicted.lower())
                true_labels.append(target_label)
                original_texts.append(text_segments[0])

    logger.info(f"accuracy = {correct/total}")
    results_df = pd.DataFrame({"text": original_texts, "true_label": true_labels, "predicted_label": predicted_labels})
    results_df.to_csv(output_file)
    logger.info(f"Finished experiment with output file:\n{output_file}")


if __name__ == "__main__":
    run_zero_shot()
