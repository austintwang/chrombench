import os
from abc import ABCMeta, abstractmethod
from functools import partial

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoModel, AutoModelForCausalLM, BertConfig
from scipy.stats import wilcoxon
from tqdm import tqdm
import h5py
import minlora

from .utils import onehot_to_chars


class LoRAModule(nn.Module):
    def __init__(self, model, lora_rank, lora_alpha, lora_dropout):
        super().__init__()

        lora_config = {
            nn.Embedding: {
                "weight": partial(minlora.LoRAParametrization.from_embedding, rank=lora_rank, lora_dropout_p=lora_dropout, lora_alpha=lora_alpha),
            },
            nn.Linear: {
                "weight": partial(minlora.LoRAParametrization.from_linear, rank=lora_rank, lora_dropout_p=lora_dropout, lora_alpha=lora_alpha),
            },
            nn.Conv1d: {
                "weight": partial(minlora.LoRAParametrization.from_conv2d, rank=lora_rank, lora_dropout_p=lora_dropout, lora_alpha=lora_alpha),
            },
        }

        self.model = model
        minlora.add_lora(self.model, lora_config=lora_config)

    def parameters(self):
        return list(minlora.get_lora_params(self.model))

    def state_dict(self):
        return minlora.get_lora_state_dict(self.model)


class HFClassifierModel(nn.Module):
    def __init__(self, tokenizer, model):
        super().__init__()

        self.model = model
        self.tokenizer = tokenizer

        device_indicator = torch.empty(0)
        self.register_buffer("device_indicator", device_indicator)
        
    def _tokenize(self, seqs):
        seqs_str = onehot_to_chars(seqs)
        encoded = self.tokenizer(seqs_str, return_tensors="pt", padding=True)
        tokens = encoded["input_ids"]

        return tokens.to(self.device)

    @property
    def device(self):
        return self.device_indicator.device

    def forward(self, seqs):
        tokens = self._tokenize(seqs)

        torch_outs = self.model(
            tokens,
            output_hidden_states=True
        )
        logits = torch_outs.logits

        return logits
