from omegaconf import DictConfig
from transformers import LlamaForCausalLM, AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os
import numpy as np
import random

from fallacy_detection.prompts.prompt import get_logic_prompt, get_multi_round_prompt
from fallacy_detection.data.definitions import FallacyClass


class Settings:
    def __init__(self, cfg: DictConfig) -> None:
        self.cfg: DictConfig = cfg
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def get_model_from_hf(self):
        model_name = self.cfg.model.name
        if "llama" in model_name:
            model = LlamaForCausalLM.from_pretrained(
                model_name, token=os.environ["llama_hf_token"], torch_dtype=torch.bfloat16, device_map="auto",
            )
        elif "mistral" or "falcon" in model_name:
            model = AutoModelForCausalLM.from_pretrained(
                model_name, token=os.environ["general_hf_token"], torch_dtype=torch.bfloat16, device_map="auto"
            )
        else:
            raise NotImplementedError
        return model

    def get_pipeline_from_hf(self):
        model_name = self.cfg.model.name
        my_pipeline = pipeline(
            "text-generation",
            model=model_name,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device=self.device,
        )
        return my_pipeline

    def get_tokenizer_from_hf(self):
        model_name = self.cfg.model.name
        if "llama" in model_name:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name, token=os.environ["llama_hf_token"], torch_dtype=torch.bfloat16, device_map="auto"
            )
            tokenizer.pad_token = tokenizer.eos_token
        elif "mistral" or "falcon" in model_name:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name, token=os.environ["general_hf_token"], device_map="auto"
            )
        else:
            raise NotImplementedError
        return tokenizer

    def get_model_inputs(self, tokenizer: AutoTokenizer, segments: list[str], device):
        model_name = self.cfg.model.name
        include_definitions = self.cfg.prompt.definitions
        fallacy_class = FallacyClass(self.cfg.prompt.fallacy_classes)
        prompt_option = self.cfg.prompt.option
        cot = self.cfg.prompt.cot
        prompts = [
            f"{get_logic_prompt(option=prompt_option,fallacy_class=fallacy_class, cot = cot, include_definitions=include_definitions,segment=segment)}{tokenizer.eos_token if 'llama' in model_name else ''}"
            for segment in segments
        ]

        if "llama" in model_name:
            encoding = tokenizer(
                prompts[0],
                # truncation=True,
                # padding=True,
                return_tensors="pt",
            )
        elif "mistral" or "falcon" in model_name:
            encoding = tokenizer(
                prompts[0],
                # truncation=True,
                # padding=True,
                return_tensors="pt",
            )
        else:
            raise NotImplementedError

        # input_ids = encoding["input_ids"].to(device)
        # attention_mask = encoding["attention_mask"].to(device)
        return encoding.to(device)

    def get_messages(self, segments: list[str], response: str = None):
        model_name = self.cfg.model.name
        include_definitions = self.cfg.prompt.definitions
        fallacy_class = FallacyClass(self.cfg.prompt.fallacy_classes)
        prompt_option = self.cfg.prompt.option
        cot = self.cfg.prompt.cot
        messages = [
            get_multi_round_prompt(
                option=prompt_option,
                response=response,
                fallacy_class=fallacy_class,
                include_definitions=include_definitions,
                segment=segment,
            )
            for segment in segments
        ]
        # prompt = pipeline.tokenizer.apply_chat_template(
        #     messages, tokenize=False, add_generation_prompt=True
        # )
        return messages

    @staticmethod
    def set_seed(seed=42):
        random.seed(seed)
        os.environ["PYHTONHASHSEED"] = str(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
