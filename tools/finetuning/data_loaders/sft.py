import torch
import copy
import os
import random
from tqdm import tqdm
from datasets import load_dataset
from transformers import PreTrainedTokenizer
from typing import Optional, Sequence, Dict, List, Tuple, Any
from torch.utils.data import Dataset
from .utils import tokenize_fn, jload
from .load_hf_instruction_data import *


HF_DATA_LIST = {
    "kyujinpy/KOpen-platypus": KOpenPlatypus
}



class SFTDataset(Dataset):
    def __init__(self,
                 tokenizer: PreTrainedTokenizer,
                 data_config: dict,
                 shuffle: bool = True,
                 ignore_index: int = -100,
                 is_hf: bool = True,
                 data_name: str = "",
                 train_or_test: str = 'train'):
        self.tokenizer = tokenizer
        self.data_config = data_config
        self.ignore_index = ignore_index
        if is_hf:
            if data_name not in list(HF_DATA_LIST.keys()):
                raise ModuleNotFoundError("지원하지 않는 데이터입니다.")
            try:
                self.list_data_dict = HF_DATA_LIST[data_name](cache_dir=data_config.cache_dir, data_type=train_or_test)
            except:
                return None
        else:
            if train_or_test == 'train':
                data_path = self.data_config['train_path']
            else:
                data_path = self.data_config['eval_path']
            # load jsonl files
            self.list_data_dict = jload(data_path)
            if shuffle and train_or_test == 'train':
                random.shuffle(self.list_data_dict)

    def preprocess_translation(
            self,
            sources: Sequence[str],
            targets: Sequence[str],
            tokenizer: PreTrainedTokenizer,
    ) -> Dict:
        examples = [s + t for s, t in zip(sources, targets)]
        examples_tokenized, sources_tokenized = [tokenize_fn(strings, tokenizer) for strings in (examples, sources)]
        input_ids = examples_tokenized["input_ids"]
        labels = copy.deepcopy(input_ids)

        if self.data_config.ignore_bp_ins_token:
            for label, source_len in zip(labels, sources_tokenized["input_ids_lens"]):
                label[:source_len] = self.ignore_index
        return dict(input_ids=input_ids, labels=labels)

    def __len__(self):
        return len(self.list_data_dict)

    def __getitem__(self, i) -> Dict[str, torch.Tensor]:
        s = [self.list_data_dict[i][self.data_config.instruction_key]]
        t = [f"{self.list_data_dict[i][self.data_config.answer_key]}{self.tokenizer.eos_token}"]

        out = self.preprocess_translation(s, t, self.tokenizer)
        return dict(input_ids=out['input_ids'][0], labels=out['labels'][0])


class DataCollatorSFTDataset:
    def __init__(self, tokenizer: PreTrainedTokenizer, ignore_index: int = -100):
        self.tokenizer = tokenizer
        self.ignore_index = ignore_index

    def __call__(self, instances: Sequence[Dict]) -> Dict[str, torch.Tensor]:
        input_ids, labels = tuple([instance[key] for instance in instances] for key in ("input_ids", "labels"))
        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids, batch_first=True, padding_value=self.tokenizer.pad_token_id
        )
        labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=self.ignore_index)
        return dict(
            input_ids=input_ids,
            labels=labels,
            attention_mask=input_ids.ne(self.tokenizer.pad_token_id),
        )
