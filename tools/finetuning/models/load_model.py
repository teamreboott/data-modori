import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from typing import Tuple
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model

def load_peft_models(base_dir: str,
                     model_name_or_path: str,
                     llm_config: dict,
                     max_len: int,
                     dpo: bool = False) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    n_gpus = torch.cuda.device_count()
    print(f"{n_gpus} Found.")
    if not llm_config['is_hf']:
        if not os.path.exists(os.path.join(base_dir, model_name_or_path)):
            raise ValueError("모델 경로를 확인해주세요.")
        else:
            model_name_or_path = os.path.join(base_dir, model_name_or_path)

    if llm_config["bits"] == 8:
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            load_in_8bit=True,
            quantization_config=bnb_config,
            device_map={"": 0},
            cache_dir=llm_config.cache_dir
        )
    else:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            load_in_4bit=True,
            device_map="auto",#{"": 0},
            quantization_config=bnb_config,
            cache_dir=llm_config.cache_dir
        )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)
    peft_config = LoraConfig(
        r=32,
        lora_alpha=64,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
            "lm_head",
        ],
        bias="none",
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, peft_config)
    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        model_max_length=max_len,
        padding_side="right",
        use_fast=False,
    )

    tokenizer.add_special_tokens(
        {
            "eos_token": "</s>",
            "bos_token": "</s>",
            "unk_token": "</s>",
            "pad_token": "</s>",
        }
    )
    return model, tokenizer, peft_config