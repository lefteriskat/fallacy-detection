from omegaconf import DictConfig
import pandas as pd
from torch.utils.data import Dataset


def new_label(label: str):
    label = label.title().replace("Of", "of")

    label = label.replace("To", "to")

    return label


def preprocess_dataframe(dataframe: pd.DataFrame):
    dataframe = dataframe[["source_article", "updated_label", "coarse_label"]]
    dataframe = dataframe[dataframe["updated_label"] != "miscellaneous"]
    dataframe["updated_label"] = dataframe["updated_label"].map(new_label)
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
        segment = self.dataframe.loc[idx, "source_article"]
        label = self.dataframe.loc[idx, "updated_label"]
        coarse_label = self.dataframe.loc[idx, "coarse_label"]

        return {
            "segment": segment,
            "label": label,
            "coarse_label": coarse_label,
        }
