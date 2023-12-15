# Data-Modori

## Korean Instruction Dataset

### Supervised Fine-Tuning with LoRA

#### Arguments
```yaml
MODE: 'train'
BASE_DIR: "/home/minsung/workspace/nas_data/"                 # base dir
SAVE_DIR: "/home/minsung/workspace/nas_data/mistral_7b_sft"   # directory for saving LLM's checkpoint
MODEL_PATH: "mistralai/Mistral-7B-v0.1"                       # Huggingface Model or local path for a checkpoint

LLM:
  is_hf: true                                                 # load Huggingface model
  bits: 4                                                     # x-bit quantization
  cache_dir: "${BASE_DIR}"                                    # cache_dir for saving Huggingface model  

DATASET:
  dataset: "kyujinpy/KOpen-platypus"                          # dataset in Huggingface Datasets
  is_hf: true                                                 # load Huggingface dataset
  instruction_key: "instruction"                              # name of key to extract instruction text in jsonl
  answer_key: "output"                                        # name of key to extract output text in jsonl
  train_path: none                                            # custom train dataset (jsonl format)
  eval_path: none                                             # custom eval dataset (jsonl format)
  cache_dir: ${BASE_DIR}                                      # cache directory for saving Huggingface Datasets
  ignore_bp_ins_token: true                                   # ignore gradient of instruction tokens in the SFT step 

TRAINER:
  optim: "paged_adamw_8bit"                                   # optimizer
  model_max_length: 2048                                      # maximum sequence length. Sequences will be right padded (and possibly truncated)
  per_device_train_batch_size: 2                              # batch size per GPU/TPU/MPS/NPU core/CPU for training
  per_device_eval_batch_size: 2                               # batch size per GPU/TPU/MPS/NPU core/CPU for evaluation
  num_train_epochs: 3                                         # total number of training epochs to perform
  warmup_steps: 100                                           # linear warmup over warmup_steps
  logging_steps: 1                                            # log every X updates steps. Should be an integer or a float in range `[0,1)`
  lr_scheduler_type: 'cosine'                                 # learning rate scheduler
  fp16: false                                                 # whether to use fp16 (mixed) precision instead of 32-bit
  bf16: true                                                  # whether to use bp16 (mixed) precision instead of 32-bit
  learning_rate: 1e-5                                         # the initial learning rate for the optimizer
  report_to: "wandb"                                          # choices = {'tensorboard', 'wandb', none}
  save_steps: 50000                                           # save ckpt
  gradient_checkpointing: true                                # if True, use gradient checkpointing to save memory at the expense of slower backward pass
  use_neft: true

WANDB:
  PROJECT_NAME: "Mistral_LORA"                                # wandb project name
  NAME: "LLaMA_7B_QLoRA_Test"                                 # wandb experiment name in project
  SAVE_CKPT: false
```

#### Run
```bash
# Mistral 7B with LoRA
sh scripts/run_mistral_lora_sft.sh
```



### DPO with LoRA

#### Arguments
```yaml
MODE: 'train'
BASE_DIR: "/home/minsung/workspace/nas_data/"                     # base dir
SAVE_DIR: "/home/minsung/workspace/nas_data/mistral_7b_dpo"       # directory for saving LLM's checkpoint
MODEL_PATH: "mistralai/Mistral-7B-v0.1"                           # Huggingface Model or local path for a checkpoint

LLM:
  is_hf: true                                                     # load Huggingface model
  bits: 4                                                         # x-bit quantization
  cache_dir: ${BASE_DIR}                                          # cache_dir for saving Huggingface model  

DATASET:
  dataset: "Intel/orca_dpo_pairs"                                 # dataset in Huggingface Datasets
  is_hf: true                                                     # load Huggingface dataset
  chosen_key: "chosen"                                            # name of key to extract instruction text in jsonl
  rejected_key: "rejected"                                        # name of key to extract output text in jsonl
  train_path: none                                                # custom train dataset (jsonl format)
  eval_path: none                                                 # custom eval dataset (jsonl format)
  cache_dir: ${BASE_DIR}

TRAINER:
  optim: "paged_adamw_8bit"                                       # optimizer
  model_max_length: 2048                                          # maximum sequence length. Sequences will be right padded (and possibly truncated)
  per_device_train_batch_size: 2                                  # batch size per GPU/TPU/MPS/NPU core/CPU for training
  per_device_eval_batch_size: 2                                   # batch size per GPU/TPU/MPS/NPU core/CPU for evaluation
  num_train_epochs: 3                                             # total number of training epochs to perform
  warmup_steps: 100                                               # linear warmup over warmup_steps
  logging_steps: 1                                                # log every X updates steps. Should be an integer or a float in range `[0,1)`
  lr_scheduler_type: 'cosine'                                     # learning rate scheduler
  fp16: false                                                     # whether to use fp16 (mixed) precision instead of 32-bit
  bf16: true                                                      # whether to use bp16 (mixed) precision instead of 32-bit
  learning_rate: 1e-5                                             # the initial learning rate for the optimizer
  report_to: "wandb"                                              # choices = {'tensorboard', 'wandb', none}
  save_steps: 50000                                               # save ckpt
  gradient_checkpointing: true                                    # if True, use gradient checkpointing to save memory at the expense of slower backward pass
  use_neft: true                                                  # NEFTUNE: NOISY EMBEDDINGS IMPROVE INSTRUCTION FINETUNING

DPO:
  beta: 0.1                                                       # the beta factor in DPO loss. Higher beta means less divergence from the initial policy.


WANDB:
  PROJECT_NAME: "Mistral_LORA"                                    # wandb project name
  NAME: "LLaMA_7B_DPO_Test"                                       # wandb experiment name in project
  SAVE_CKPT: false
```


#### Run
```bash
# Mistral 7B with LoRA
sh scripts/run_mistral_lora_dpo.sh
```

