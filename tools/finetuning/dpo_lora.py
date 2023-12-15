import argparse
import os
from omegaconf import OmegaConf
from models.load_model import load_peft_models
from transformers import TrainingArguments
from data_loaders import load_dpo_dataset_from_hf
from typing import Optional, Dict
from dataclasses import dataclass, field
from trl import DPOTrainer
from typing import Optional


@dataclass
class TrainingArguments(TrainingArguments):
    cache_dir: Optional[str] = field(default=None)
    optim: str = field(default="paged_adamw_8bit")
    output_dir: str = field(default="output/")
    model_max_length: int = field(
        default=4096,
        metadata={"help": "Maximum sequence length. Sequences will be right padded (and possibly truncated)."},
    )
    per_device_train_batch_size: int = field(
        default=1, metadata={"help": "Batch size per GPU/TPU/MPS/NPU core/CPU for training."}
    )
    per_device_eval_batch_size: int = field(
        default=32, metadata={"help": "Batch size per GPU/TPU/MPS/NPU core/CPU for evaluation."}
    )
    num_train_epochs: float = field(default=3.0, metadata={"help": "Total number of training epochs to perform."})
    warmup_steps: int = field(default=2, metadata={"help": "Linear warmup over warmup_steps."})
    save_steps: int = field(default=2000, metadata={"help": "Save CKPT over save_steps."})
    logging_steps: float = field(
        default=1,
        metadata={
            "help": (
                "Log every X updates steps. Should be an integer or a float in range `[0,1)`."
                "If smaller than 1, will be interpreted as ratio of total training steps."
            )
        },
    )
    lr_scheduler_type: Optional[str] = field(default='cosine')
    fp16: bool = field(
        default=False,
        metadata={"help": "Whether to use fp16 (mixed) precision instead of 32-bit"},
    )
    bf16: bool = field(
        default=True,
        metadata={"help": "Whether to use bf16 (mixed) precision instead of 32-bit"},
    )
    learning_rate: float = field(default=1e-5, metadata={"help": "The initial learning rate for AdamW."})

    report_to: Optional[str] = field(default='wandb')
    gradient_checkpointing: bool = field(
        default=True,
        metadata={
            "help": "If True, use gradient checkpointing to save memory at the expense of slower backward pass."
        },
    )
    run_name: Optional[str] = field(default='debug')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My training script.')
    parser.add_argument('--local_rank', type=int, default=-1,
                        help='local rank passed from distributed launcher')
    parser.add_argument("--cmd_config_path", default='./config/mistral_7b_lora_dpo.yaml', type=str)
    args = parser.parse_args()
    config = OmegaConf.load(args.cmd_config_path)

    # Fine-tuning process
    if config.MODE == 'train':
        # wandb logger
        os.environ["WANDB_PROJECT"] = config.WANDB.PROJECT_NAME  # name your W&B project
        if config.WANDB.SAVE_CKPT:
            os.environ["WANDB_LOG_MODEL"] = "checkpoint"  # log all model checkpoints

        # model loads
        model, tokenizer, peft_config = load_peft_models(base_dir=config.BASE_DIR,
                                                         model_name_or_path=config.MODEL_PATH,
                                                         llm_config=config.LLM,
                                                         max_len=config.TRAINER.model_max_length, dpo=True)
        
        model_ref, _, _ = load_peft_models(base_dir=config.BASE_DIR,
                                           model_name_or_path=config.MODEL_PATH,
                                           llm_config=config.LLM,
                                           max_len=config.TRAINER.model_max_length, dpo=True)

        # build dataset
        train_dataset = load_dpo_dataset_from_hf(dataset_name=config.DATASET.dataset,
                                                 sanity_check=False,
                                                 cache_dir=config.DATASET.cache_dir,
                                                 num_proc=24,
                                                 data_config=config.DATASET,
                                                 train_or_test='train')

        if os.path.isfile(os.path.join(config.BASE_DIR, config.DATASET['eval_path'])) or config.DATASET.is_hf:
            eval_dataset = load_dpo_dataset_from_hf(dataset_name=config.DATASET.dataset,
                                                    sanity_check=False,
                                                    cache_dir=config.DATASET.cache_dir,
                                                    num_proc=24,
                                                    data_config=config.DATASET,
                                                    train_or_test='val')
        else:
            eval_dataset = None

        # output
        os.makedirs(config.SAVE_DIR, exist_ok=True)
        last_model_ckpt = os.path.join(config.SAVE_DIR, "last_ckpt")
        os.makedirs(last_model_ckpt, exist_ok=True)

        train_args = TrainingArguments(output_dir=config.SAVE_DIR,
                                       optim=config.TRAINER['optim'],
                                       model_max_length=config.TRAINER['model_max_length'],
                                       per_device_train_batch_size=config.TRAINER['per_device_train_batch_size'],
                                       num_train_epochs=config.TRAINER['num_train_epochs'],
                                       fp16=config.TRAINER['fp16'],
                                       bf16=config.TRAINER['bf16'],
                                       save_steps=config.TRAINER['save_steps'],
                                       warmup_steps=config.TRAINER['warmup_steps'],
                                       gradient_checkpointing=config.TRAINER['gradient_checkpointing'],
                                       lr_scheduler_type=config.TRAINER['lr_scheduler_type'],
                                       learning_rate=config.TRAINER['learning_rate'],
                                       run_name=config.WANDB.NAME,
                                       report_to=config.TRAINER.report_to,
                                       )

        # PEFT
        trainer = DPOTrainer(
            model,
            model_ref,
            args=train_args,
            beta=config.DPO.beta,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer
        )
        trainer.train()
        trainer.save_model(last_model_ckpt)
        trainer.save_state()
