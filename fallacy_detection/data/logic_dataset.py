from omegaconf import DictConfig
import pandas as pd
from torch.utils.data import Dataset


def new_label(label: str):
    label = label.title().replace("Of", "of")

    label = label.replace("To", "to")

    return label


def preprocess_dataframe(dataframe: pd.DataFrame):
    dataframe = dataframe[dataframe["fallacy_type"] != "miscellaneous"]
    dataframe["fallacy_type"] = dataframe["fallacy_type"].map(new_label)
    return dataframe


class LogicDataset(Dataset):
    def __init__(self, cfg: DictConfig):
        df = pd.read_csv(cfg.data.file_path)
        df = preprocess_dataframe(df)
        self.dataframe = df

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        # Get text and label for the specified index
        text = self.dataframe.loc[idx, "text"]
        fallacy_type = self.dataframe.loc[idx, "fallacy_type"]
        copi_fallacy_type = self.dataframe.loc[idx, "copi_fallacy_type"]
        aristotle_fallacy_type = self.dataframe.loc[idx, "aristotle_fallacy_type"]

        return {
            "text": text,
            "fallacy_type": fallacy_type,
            "copi_fallacy_type": copi_fallacy_type,
            "aristotle_fallacy_type": aristotle_fallacy_type,
        }
