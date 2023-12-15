from datasets import load_dataset, Dataset
from typing import Dict


def load_dpo_dataset_from_hf(
    dataset_name: str = "lvwerra/stack-exchange-paired",
    sanity_check: bool = False,
    cache_dir: str = None,
    num_proc=24,
    data_config: dict = None,
    train_or_test: str = 'train'
) -> Dataset:
    """Load the stack-exchange-paired dataset from Hugging Face and convert it to the necessary format.

    The dataset is converted to a dictionary with the following structure:
    {
        'prompt': List[str],
        'chosen': List[str],
        'rejected': List[str],
    }
    """
    try:
        dataset = load_dataset(
            dataset_name,
            split=train_or_test,
            cache_dir=cache_dir,
        )
    except:
        # w/o val
        return None
    original_columns = dataset.column_names

    if sanity_check:
        dataset = dataset.select(range(min(len(dataset), 100)))

    print('dataset length = ', len(dataset))
    def return_prompt_and_responses(samples) -> Dict[str, str]:
        return {
            "prompt": [f"[INST] {q} [/INST]" for q in samples["question"]],
            "chosen": samples[data_config.chosen_key],
            "rejected": samples[data_config.rejected_key],
        }

    return dataset.map(
        return_prompt_and_responses,
        batched=True,
        num_proc=num_proc,
        remove_columns=original_columns,
    )
