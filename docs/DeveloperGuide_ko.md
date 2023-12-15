# 개발자를 위한 How-to 가이드

* [개발자를 위한 How-to 가이드](#개발자를-위한-how-to-가이드)
   * [자체 연산자 구축](#자체-연산자-구축)
   * [자체 설정 파일 구성](#자체-설정-파일-구성)
      * [풍부한 설정 소스 및 타입 힌트](#풍부한-설정-소스-및-타입-힌트)
      * [계층적인 설정 및 도움말](#계층적인-설정-및-도움말)

## 자체 연산자 구축

- **Data-modori**는 누구나 자체 연산자를 구축할 수 있도록 합니다.
- 새로운 연산자를 구현하기 전에 [Operators](Operators_ko.md) 참조하여 불필요한 중복을 피하세요.
- 새로운 "TextLengthFilter"라는 새로운 필터 연산자를 추가하려면 다음 단계를 따를 수 있습니다.

1. (선택 사항) `data_modori/utils/constant.py`에 새로운 연산자의 통계 변수를 저장하기 위한 새로운 `StatsKeys`를 추가합니다.

```python
class StatsKeys(object):
    ...              # other keys
    text_len = 'text_len'
```

2. `data_modori/ops/filter/` 디렉토리에 `text_length_filter.py`라는 새로운 연산자 파일을 다음과 같이 생성합니다.
   - 이것은 필터 연산자이므로 새로운 연산자는 기본 `Filter` 클래스에서 상속되어야 하며, 자동으로 자체를 등록하기 위해 `OPERATORS`로 데코레이트되어야 합니다.

```python
import sys

from jsonargparse.typing import PositiveInt

from data_modori.utils.constant import Fields, StatsKeys

from ..base_op import OPERATORS, Filter


@OPERATORS.register_module('text_length_filter')
class TextLengthFilter(Filter):
    """특정 범위 내의 전체 텍스트 길이를 가진 샘플을 유지하는 필터입니다."""


    def __init__(self,
                 min_len: PositiveInt = 10,
                 max_len: PositiveInt = sys.maxsize,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param min_len: 필터링에서의 최소 텍스트 길이입니다. 이 매개변수 미만의 텍스트 길이를 갖는 샘플은 필터링됩니다.
        :param max_len: 필터링에서의 최대 텍스트 길이입니다. 이 매개변수를 초과하는 텍스트 길이를 갖는 샘플은 필터링됩니다.
        :param args: 추가적인 인수
        :param kwargs: 추가적인 인수
        """
        super().__init__(*args, **kwargs)
        self.min_len = min_len
        self.max_len = max_len

    def compute_stats(self, sample):
        # 이미 계산되었는지 확인
        if StatsKeys.text_len in sample[Fields.stats]:
            return sample

        sample[Fields.stats][StatsKeys.text_len] = len(sample[self.text_key])
        return sample

    def process(self, sample):
        if self.min_len <= sample[Fields.stats][StatsKeys.text_len] <= self.max_len:
            return True
        else:
            return False
```

3. 구현 후, `data_modori/ops/filter/` 디렉토리의 `__init__.py` 파일에 이를 연산자 딕셔너리에 추가합니다.

```python
from . import (...,              # 다른 연산자들
               text_length_filter)  # 새로운 연산자 모듈을 가져옴
```

4. 이제 이 새로운 연산자를 사용자 정의 인수와 함께 자체 설정 파일에서 사용할 수 있습니다!

```yaml
# 다른 설정
...

# 처리 설정
process:
  - text_length_filter:  # 이 연산자를 처리 목록에 추가하고 매개변수를 설정합니다.
      min_len: 10
      max_len: 1000
```

## 자체 설정 파일 구성
- 우리는 [jsonargparse](https://github.com/omni-us/jsonargparse/)를 기반으로 한 쉬운 구성을 제공하여 보일러플레이트 코드의 비용을 감소시킵니다.

### 풍부한 설정 소스 및 타입 힌트
- 전역 구성 객체는 다음과 같이 초기화될 수 있습니다.
```
# core.executor.py
self.cfg = init_configs()
```
- 여기에 다양한 소스에서 함수 인수를 지정하고 섞을 수 있습니다.
1. 파서에 구성을 등록할 때 또는 클래스의 `__init__` 함수에서 지정된 경우 하드 코딩된 기본값
2. json (yaml 또는 jsonnet의 상위 집합)의 기본 구성 파일
3. *환경 변수*
4. ``--project_name my_data_demo`` 또는 ``--project_name=my_data_demo``와 같은 *POSIX-스타일의 명령 줄 인수* (구성 파일 포함)

- 최종 구문된 값은 이러한 소스에서 섞입니다. 그리고 재정렬 순서는 위의 번호와 같습니다.

또한 다양한 인수 유형 및 해당 유효성 검사가 지원됩니다.
파이썬 내장 유형, [Lib/typing](https://docs.python.org/3/library/typing.html) 모듈의 유형 및
jsonargparse의 확장 [유형](https://jsonargparse.readthedocs.io/en/stable/#type-hints),
예를 들면 `restricted types` 및 사용자 정의된 제한이 있는 `Paths`와 같은 것들이 있습니다.

### 계층적인 설정 및 도움말
-인수 이름에서 계층을 정의하는 데 점 표기법을 자유롭게 사용할 수 있습니다.
가령 `maximum_line_length_filter.min`와 같이 정의할 수 있습니다.
무엇보다 중요한 것은 기본적으로 모든 구성의 구조가 구현된 연산자의 독스트링에서 자동으로 등록된다는 것입니다.
즉, 모든 구성의 구조는 항상 코드와 동기화되어 있습니다.

- 실행기를 호출하는 스크립트를 실행하여 계층적인 도움말 정보를 얻을 수 있습니다.
```
$ python tools/process_data.py --help

usage: process_data.py [-h] [--config CONFIG] [--print_config[=flags]] [--project_name PROJECT_NAME] [--dataset_path DATASET_PATH] [--dataset_dir DATASET_DIR] [--export_path EXPORT_PATH] [--process PROCESS]
                            [--np NP] [--text_keys TEXT_KEYS] [--document_deduplicator CONFIG] [--document_deduplicator.hash_method HASH_METHOD] [--document_deduplicator.lowercase LOWERCASE]
                            [--document_deduplicator.ignore_non_character IGNORE_NON_CHARACTER] [--language_id_score_filter CONFIG] [--language_id_score_filter.lang LANG] [--words_num_filter CONFIG] [--words_num_filter.min MIN] [--words_num_filter.max MAX]
                            [--alphanumeric_filter CONFIG] [--alphanumeric_filter.min MIN] [--alphanumeric_filter.max MAX] [--average_line_length_filter CONFIG] [--average_line_length_filter.min MIN] [--average_line_length_filter.max MAX]
                            [--maximum_line_length_filter CONFIG] [--maximum_line_length_filter.min MIN] [--maximum_line_length_filter.max MAX] [--text_length_filter CONFIG] [--text_length_filter.min MIN] [--text_length_filter.max MAX]
                            [--remove_comments_mapper CONFIG] [--remove_comments_mapper.type TYPE] [--remove_comments_mapper.inline INLINE] [--remove_comments_mapper.multiline MULTILINE] [--remove_header_mapper CONFIG]
                            [--remove_header_mapper.before_section BEFORE_SECTION]

optional arguments:
  -h, --help            Show this help message and exit.
  --config CONFIG       Path to a configuration file.
  --print_config[=flags]
                        Print the configuration after applying all other arguments and exit. The optional flags customizes the output and are one or more keywords separated by comma. The supported flags are: comments, skip_default, skip_null.
  --project_name PROJECT_NAME
                        name of your data process project. (type: str, default: null)
  --dataset_path DATASET_PATH
                        path to your dataset file, relative with respect to the config file’s location (type: Path_fr, default: null)
  --dataset_dir DATASET_DIR
                        path to your dataset(s) within a directory, relative with respect to the config file’s location (type: Path_drw, default: null)
  --export_path EXPORT_PATH
                        path to the output processed dataset, relative with respect to the config file’s location (type: Path_fc, default: null)
  --process PROCESS, --process+ PROCESS
                        a list of several process operators with their arguments (type: List[Dict], default: null)
  --np NP               number of subprocess to process your dataset. (type: PositiveInt, default: null)

<class 'data_modori.ops.filter.alphanumeric_filter.AlphanumericFilter'>:
  --alphanumeric_filter CONFIG
                        Path to a configuration file.
  --alphanumeric_filter.min MIN
                        the min filter rate in alphanumeric op. (type: ClosedUnitInterval, default: 0.0)
  --alphanumeric_filter.max MAX
                        the max filter rate in alphanumeric op. (type: ClosedUnitInterval, default: 0.25)

<class 'data_modori.ops.filter.text_length_filter.TextLengthFilter'>:
  --text_length_filter CONFIG
                        Path to a configuration file.
  --text_length_filter.min MIN
                        min text length in the filtering (type: int, default: 10)
  --text_length_filter.max MAX
                        max text length in the filtering (type: int, default: 10000)

......

```
