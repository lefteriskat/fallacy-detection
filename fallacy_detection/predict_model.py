from omegaconf import DictConfig, OmegaConf
import hydra
import pandas as pd
from tqdm import tqdm

from fallacy_detection.data.logic_dataset import LogicDataset
from fallacy_detection.utils.settings import Settings

from torch.utils.data import DataLoader
import torch
from accelerate import Accelerator


@hydra.main(version_base=None, config_path="../config", config_name="config")
def predict(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    settings = Settings(cfg)
    accelerator = Accelerator()
    device = accelerator.device
    print(device)
    tokenizer = settings.get_tokenizer_from_hf()
    model = settings.get_model_from_hf()
    model.generation_config.pad_token_id = tokenizer.pad_token_id

    logic_dataset = LogicDataset(cfg)

    coarse_grained_classification = cfg.prompt.coarse_grained_classification

    model.eval()
    # Create the DataLoader
    batch_size = 1  # Set batch size as needed
    dataloader = DataLoader(logic_dataset, batch_size=batch_size, shuffle=False)
    total = 0
    correct = 0
    predicted_labels = []
    true_labels = []
    source_articles = []
    for batch in tqdm(dataloader):
        segments = batch["segment"]
        labels = batch["label"]
        coarse_labels = batch["coarse_label"]
        with torch.no_grad():
            # Generate predictions
            input_ids, attention_mask = settings.get_model_inputs(tokenizer, segments, device)

            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                # temperature = 0.8,
                max_new_tokens=50,
            )

            # Decode and print output
            for i in range(len(outputs)):
                prompt_length = input_ids[0].shape[0]
                predicted_all = tokenizer.decode(
                    outputs[i], skip_special_tokens=True, clean_up_tokenization_spaces=True
                )
                predicted = tokenizer.decode(
                    outputs[i][prompt_length:], skip_special_tokens=True, clean_up_tokenization_spaces=True
                )

                if coarse_grained_classification:
                    target_label = coarse_labels[i].lower()
                else:
                    target_label = labels[i].lower()

                if total % 10 == 0:
                    print("Generated Text:", predicted_all)
                    print("Predicted_label:", predicted)
                    print("True Label: ", target_label)
                total += 1

                if target_label in predicted.lower():
                    correct += 1
                predicted_labels.append(predicted.lower())
                true_labels.append(target_label)
                source_articles.append(segments[0])

    print(f"accuracy = {correct/total}")
    results_df = pd.DataFrame(
        {"source_article": source_articles, "true_label": true_labels, "predicted_label": predicted_labels}
    )
    results_df.to_csv(
        f"reports/{str(cfg.model.name).replace('/', '-')}_{'coarse_grained' if cfg.prompt.coarse_grained_classification else 'fine_grained'}_results{'_with_definitions' if cfg.prompt.definitions else '_no_definitions'}.csv"
    )


if __name__ == "__main__":
    predict()
