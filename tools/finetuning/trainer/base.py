import torch
from trl import SFTTrainer


class FullTrainer(SFTTrainer):

    def _prepare_dataset(
            self,
            dataset,
            tokenizer,
            packing,
            dataset_text_field,
            max_seq_length,
            formatting_func,
            infinite,
            num_of_sequences,
            chars_per_token,
    ):
        if dataset is None:
            raise ValueError("The dataset should not be None")

        # check if torch dataset / dataloader and do nothing
        if isinstance(dataset, (torch.utils.data.IterableDataset, torch.utils.data.Dataset)):
            return dataset
        else:
            raise NotImplementedError


