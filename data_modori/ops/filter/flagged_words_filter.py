# Some code here has been modified from:
# https://huggingface.co/spaces/huggingface/text-data-filtering
# --------------------------------------------------------

from jsonargparse.typing import ClosedUnitInterval, List

from data_modori.utils.constant import Fields, StatsKeys, InterVars
from data_modori.utils.model_utils import prepare_model, get_model

from ...utils.asset_utils import ASSET_DIR, load_words_asset
from ..base_op import OPERATORS, Filter
from ..op_fusion import INTER_WORDS
from ..common import (SPECIAL_CHARACTERS, get_words_from_document,
                      words_refinement)


@OPERATORS.register_module('flagged_words_filter')
@INTER_WORDS.register_module('flagged_words_filter')
class FlaggedWordFilter(Filter):
    """Filter to keep samples with flagged-word ratio less than a specific max
    value."""

    def __init__(self,
                 lang: str = 'en',
                 tokenization: bool = False,
                 max_ratio: ClosedUnitInterval = 0.045,
                 flagged_words_dir: str = ASSET_DIR,
                 use_words_aug: bool = False,
                 words_aug_group_sizes: List = [2],
                 words_aug_join_char: str = '',
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param lang: Consider flagged words in what language. If lang ==
            "all", we will adopt the one merged from all the available
            languages
        :param tokenization: Whether to use model to tokenize documents
        :param max_ratio: The max filter ratio in this op.
        :param flagged_words_dir: The directory storing the
            flagged_words file(s) whose name includes "flagged_words"
            and in json format
        :param use_words_aug: Whether to augment words, especially for
            Chinese and Vietnamese
        :param words_aug_group_sizes: The group size of words to augment
        :param words_aug_join_char: The join char between words to
            augment
        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)
        self.lang = lang
        self.max_ratio = max_ratio
        self.use_words_aug = use_words_aug
        self.words_aug_group_sizes = words_aug_group_sizes
        self.words_aug_join_char = words_aug_join_char
        self.model_key = None
        self.lang = lang

        self.FLAGGED_WORDS = load_words_asset(words_dir=flagged_words_dir,
                                              words_type='flagged_words')

        if 'all' not in self.FLAGGED_WORDS:
            self.FLAGGED_WORDS['all'] = [
                val for vals in self.FLAGGED_WORDS.values() for val in vals
            ]
        if tokenization:
            self.model_key = prepare_model(lang=lang,
                                           model_type='sentencepiece')

    def compute_stats(self, sample, context=False):
        # check if it's computed already
        if StatsKeys.flagged_words_ratio in sample[Fields.stats]:
            return sample

        # try to get words from context
        words_key = f'{InterVars.words}-{self.model_key}'
        if context and words_key in sample[Fields.context]:
            words = sample[Fields.context][words_key]
        else:
            tokenizer = get_model(self.model_key, lang=self.lang, model_type='sentencepiece')

            if self.lang == 'en':
                words = get_words_from_document(
                    sample[self.text_key],
                    token_func=tokenizer.encode_as_pieces if tokenizer else None)
            else:
                words = get_words_from_document(sample[self.text_key], token_func=tokenizer if tokenizer else None)
            if context:
                sample[Fields.context][words_key] = words

        # try to get refined words from context
        refined_words_key = f'{InterVars.refined_words}-True-SPECIAL_CHARS-' \
                            f'{self.use_words_aug}-' \
                            f'{self.words_aug_group_sizes}-' \
                            f'{self.words_aug_join_char}'
        if context and refined_words_key in sample[Fields.context]:
            words = sample[Fields.context][refined_words_key]
        else:
            words = words_refinement(
                words,
                lower_case=True,
                strip_chars=SPECIAL_CHARACTERS,
                use_words_aug=self.use_words_aug,
                words_aug_group_sizes=self.words_aug_group_sizes,
                words_aug_join_char=self.words_aug_join_char)
            if context:
                sample[Fields.context][refined_words_key] = words
        
        if self.lang == "ko":
            FLAGGED_WORDS_LIST = ['간나', '갈보', '개', '개년', '개돼지', '개새끼', '개쓰레기', '개소리', '개씨발', '개자식', '개지랄', '개판', '개차반', '거지새끼', '거렁뱅이', '걸레', '꼬걸', '게이', '경을칠놈', '고자', '과메기', '광녀', '괴뢰', '괴뢰군', '귓것', '그지깽깽이', '금붕어', '급식충', '김치녀', '깝치다', '깜둥이', '꺼벙이', '꺼져', '꼬라보다', '꼬붕', '꼰대', '꼴불견', '꼴통', '남창', '냄비', '네 다음 XX', 'ㄴㄷㅆ', '놈', '년', '연놈', '논다니', '눈 깔아', '니 XX(패드립)', '니애미', '니미', '니애비', '느금마', '느개비', '너검엄빠', '니미럴', '니미뽕', '니거', '니기미', '나가 죽어', '나가 뒤져', '닥쳐', '닭', '새', '돌', '빡+~대가리', '덜떨어지다', '돌았다', '또라이', '돼지', '돼지새끼', '돼새', '되놈', '두루애', '뒈지다', '등신', '따까리', '딸딸이', '땡중', '땡추', '떨거지', '똘마니', '똘추', '똥', '똥개', '똥꼬충', '띨빵', '띨띨이', '레기', '렉카충', '로리콘', '루저', '라져', '말하는 가축', '망나니', '맘충', '매국노', '머저리', '먹사', '멍청도', '멍청이', '메갈리아', '멧돼지', '모자라다', '몸빵', '무뇌', '미제', '미치광이', '미친', '미친개', '미친놈', '미친년', '미친새끼', '박쥐', '박쥐짓', '박쥐같은 새끼', '바보', '바보멍청이해삼멍게말미잘', '반푼이', '벌레', '버러지', '변태', '변태새끼', '병신', '븅딱', '보지', '보슬(아치)', '보전깨', '보추', '보빨러', '버팔로', '불알', '부랄', '부모 홀수인 새끼', '불한당', '비틱', '빌어먹을', '빠가', '빠구리', '빠돼쌍', '빡추', '빨갱이', '빨통', '빻다', '뻐큐', '삐꾸', '사이버 렉카', '사이코', '상판대기', '상폐녀', '상폐놈', '상폐년', '삼엽충', '삼성빠돌이', '쇼타콘', '새끼', '석녀', '설명충', '솔개', '쇠똥구리', '수전노', '십장생', '싸가지', '쌍놈', '쌍년', '쌍노무새끼', '쌍욕', '썅', '썅년', '썩을', '쓰레기', '씨발', '씨방새', '씨방놈', '씨방년', '씨방짭새', '씨부랄', '씨벌탱', '섊', '씹', '씹년', '씹덕', '씹새끼', '씹쓰레기', '씹지랄', '씹창', '씹치남', '아가리', '아닥', '아다', '애미', '애비', '애비충', '애새끼', '애자', '양놈', '양반', '어저미', '언년이', '얼간이', '엿', '에라이', '앰흑', '엠창', '엠창인생', '옌장', '열폭', '염병', '오랑캐', '오유충', '왜놈', '우라질', '운지', '워마드', '육갑떨다', '육갑하다', '육변기', '육시랄', '이완용', '일베충', '자지', '잡놈', '잡종', '장뚜룸', '장애인', '재수가 없다', '잼민이', '저능아', '전두환', '정박아', '정신병자', '젖', '제기랄', '젠장', '조센징', '좆', '좆같다', '좆까', '좆나', '좆도 아닌 새끼', '좆간지', '좆물', '좆밥', '좆만이', '좆대가리', '좆심', '좆집', '좆병신', '좆빨러', '주둥이', '쥐새끼', '지기미', '지랄', '짜져 있어', '짱깨', '쩌리', '쪼다', '쪽발이', '쫄보', '찌질이', '찐따', '찐찌버거', '창녀', '창남', '창놈', '별창', '천치', '촛불좀비', '최순실', '추남', '추녀', '~충', '철면피', '코쟁이', '코흘리개', '~퀴', '문퀴벌레', '외퀴', '토착왜구', '통구이드립', '튀기', '트롤', '틀딱', '틀', '파쇼', '폐급', '폐녀자', '폐인', '피싸개', '한남', '한남충', '한녀', '한녀충', '허접', '허접쓰레기', '호구', '호랑말코', '호로', '후레자식', '호모', '홍어', '화냥년', '후빨', '흑돼지']
        else:
            FLAGGED_WORDS_LIST = self.FLAGGED_WORDS[self.lang]

        flagged_words_ratio = (len(
            [word
             for word in words if word.replace("▁", "") in FLAGGED_WORDS_LIST]) /
                               len(words)) if len(words) != 0 else 0.0

        if flagged_words_ratio > 1.0:
            flagged_words_ratio = 1.0

        sample[Fields.stats][
            StatsKeys.flagged_words_ratio] = flagged_words_ratio
        return sample

    def process(self, sample):
        return sample[Fields.stats][
            StatsKeys.flagged_words_ratio] <= self.max_ratio
