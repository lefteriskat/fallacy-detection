from omegaconf import DictConfig
from transformers import LlamaForCausalLM, AutoModelForCausalLM, AutoTokenizer
import torch
import os

from fallacy_detection.data.llama_prompts_logic import get_logic_prompt, delimiter


class Settings:
    def __init__(self, cfg: DictConfig) -> None:
        self.cfg: DictConfig = cfg
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def get_model_from_hf(self):
        model_name = self.cfg.model.name
        if "llama" in model_name:
            model = LlamaForCausalLM.from_pretrained(
                model_name, token=os.environ["llama_hf_token"], torch_dtype=torch.bfloat16, device_map="auto"
            )
        elif "mistral" in model_name:
            model = AutoModelForCausalLM.from_pretrained(
                model_name, token=os.environ["general_hf_token"], torch_dtype=torch.bfloat16, device_map="auto"
            )
        else:
            raise NotImplementedError
        return model

    def get_tokenizer_from_hf(self):
        model_name = self.cfg.model.name
        if "llama" in model_name:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name, token=os.environ["llama_hf_token"], torch_dtype=torch.bfloat16, device_map="auto"
            )
            tokenizer.pad_token = tokenizer.eos_token
        elif "mistral" in model_name:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name, token=os.environ["general_hf_token"], device_map="auto"
            )
        else:
            raise NotImplementedError
        return tokenizer

    def get_model_inputs(self, tokenizer: AutoTokenizer, segments: list[str], device):
        model_name = self.cfg.model.name
        include_definitions = self.cfg.prompt.definitions
        coarse_grained_classification = self.cfg.prompt.coarse_grained_classification
        if "llama" in model_name:
            prompts = [
                get_logic_prompt(
                    coarse_grained=coarse_grained_classification, include_definitions=include_definitions
                ).format(delimiter=delimiter, segment=segment)
                for segment in segments
            ]
            encoding = tokenizer(
                prompts[0],
                # truncation=True,
                # padding=True,
                return_tensors="pt",
            )
            input_ids = encoding["input_ids"].to(device)
            attention_mask = encoding["attention_mask"].to(device)
        elif "mistral" in model_name:
            prompts = [
                get_logic_prompt(
                    coarse_grained=coarse_grained_classification, include_definitions=include_definitions
                ).format(delimiter=delimiter, segment=segment)
                for segment in segments
            ]
            encoding = tokenizer(
                prompts[0],
                # truncation=True,
                # padding=True,
                return_tensors="pt",
            )
            input_ids = encoding["input_ids"].to(device)
            attention_mask = encoding["attention_mask"].to(device)
        else:
            raise NotImplementedError

        return input_ids, attention_mask
