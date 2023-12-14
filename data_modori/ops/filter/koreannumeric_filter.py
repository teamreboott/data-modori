import sys

from jsonargparse.typing import PositiveFloat

from data_modori.utils.constant import Fields, StatsKeys
from data_modori.utils.model_utils import prepare_model, get_model

from ..base_op import OPERATORS, Filter
from ..common import get_words_from_document


@OPERATORS.register_module('koreannumeric_filter')
class KoreannumericFilter(Filter):
    """Filter to keep samples with alphabet/numeric ratio within a specific
    range."""

    def __init__(self,
                 tokenization: bool = False,
                 min_ratio: float = 0.25,
                 max_ratio: PositiveFloat = sys.maxsize,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param tokenization: Whether to count the ratio of alphanumeric
            to the total number of tokens. if tokenization=False, it
            will count the ratio of alphanumeric to the total number of
            characters.
        :param min_ratio: The min filter ratio in alphanumeric op,
            samples will be filtered if their alphabet/numeric ratio is
            below this parameter.
        :param max_ratio: The max filter ratio in alphanumeric op,
            samples will be filtered if their alphabet/numeric ratio
            exceeds this parameter.
        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.tokenization = tokenization
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.model_key = None

        print("TESTSETSTSETSE")
        exit()

        if tokenization:
            # self.model_key = prepare_model(lang="ko",
            #                     model_type='konlpy')
            self.model_key = prepare_model(
                model_type='huggingface',
                model_key='quantumaikr/KoreanLM')
            

    def compute_stats(self, sample):
        if self.tokenization:
            if StatsKeys.korean_token_ratio in sample[Fields.stats]:
                return sample
            alpha_count = sum(
                map(lambda char: 1
                    if char.isalpha() else 0, sample[self.text_key]))
            tokenizer = get_model(self.model_key, model_type='huggingface')
            # tokenizer = get_model(self.model_key, lang="ko",
            #                                     model_type='konlpy')
            print(tokenizer)
            token_count = len(
                get_words_from_document(
                    sample[self.text_key],
                    token_func=tokenizer.tokenize if tokenizer else None))
                    # token_func=tokenizer.morphs if tokenizer else None))

            # print(f"{sample[self.text_key]}, alpha_count: {alpha_count}, token_count: {token_count}, {alpha_count / token_count}")
            sample[Fields.stats][StatsKeys.korean_token_ratio] = (
                alpha_count / token_count) if token_count != 0 else 0.0
        else:
            if StatsKeys.alnum_ratio in sample[Fields.stats]:
                return sample
            alnum_count = sum(
                map(lambda char: 1
                    if char.isalnum() else 0, sample[self.text_key])) # 한글에 대한 개수까지 반영됨
            sample[Fields.stats][StatsKeys.alnum_ratio] = (
                alnum_count / len(sample[self.text_key])) if len(
                    sample[self.text_key]) != 0 else 0.0
        return sample

    def process(self, sample):
        ratio = sample[Fields.stats][
            StatsKeys.korean_token_ratio] if self.tokenization else sample[
                Fields.stats][StatsKeys.alnum_ratio]
        if self.min_ratio <= ratio <= self.max_ratio:
            return True
        else:
            return False
