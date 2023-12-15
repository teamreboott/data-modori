# 전처리 도구

이 폴더에는 **Data-Modori**를 사용하기 전에 데이터셋을 추가로 처리하기 위한 몇 가지 전처리 스크립트가 포함되어 있습니다.

## 사용법

### 언어별로 데이터셋을 하위 데이터셋으로 분할

이 도구는 원시 데이터셋을 언어 정보에 따라 다른 하위 데이터셋으로 분할합니다.

```shell
python tools/preprocess/dataset_split_by_language.py        \
    --src_dir             <src_dir>          \
    --target_dir          <target_dir>       \
    --suffixes            <suffixes>         \
    --text_key            <text_key>         \
    --num_proc            <num_proc>

# 도움말 얻기
python tools/preprocess/dataset_split_by_language.py --help
```
- `src_dir`: 데이터셋을 저장하는 경로를 설정합니다.
- `target_dir`: 변환된 jsonl 파일을 저장할 결과 디렉토리입니다.
- `text_key`: 샘플 텍스트를 저장하는 필드의 키 이름입니다. 기본값: text
- `suffixes`: 읽을 파일의 접미사입니다. 기본값: None
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.

### raw arXiv 데이터를 jsonl로 변환

이 도구는 S3에서 다운로드한 raw arXiv 데이터를 **Data-Modori**에 친숙한 jsonl 형식으로 변환하는 데 사용됩니다.


```shell
python tools/preprocess/raw_arxiv_to_jsonl.py           \
    --arxiv_src_dir       <arxiv_src_dir>    \
    --target_dir          <target_dir>       \
    --temp_dir            <temp_dir>         \
    --num_proc            <num_proc>

# 도움말 얻기
python tools/preprocess/raw_arxiv_to_jsonl.py  --help
```
- `arxiv_src_dir`: raw arXiv 데이터를 Redpajama처럼 다운로드하면 `arXiv_src_yymm_xxx.tar`와 같은 파일 이름을 가진 수천 개의 tar 파일이 들어 있는 src 디렉터리를 얻게 됩니다. 이 인수를 이 디렉토리의 경로로 설정하면 됩니다.
- `target_dir`: 변환된 jsonl 파일을 저장할 결과 디렉토리입니다.
- `temp_dir`: 중간 파일을 저장하는 디렉토리이며, 변환이 끝나면 제거됩니다. 기본값은 `./tmp`입니다.
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.

**참고:**

* 다운로드 프로세스에 대해서는 [여기]((https://github.com/togethercomputer/RedPajama-Data/tree/main/data_prep/arxiv))를 참조하십시오.

* 다운로드하기 전에 변환하거나 처리하기 전에 드라이브 공간이 충분히 큰지 확인해야 할 수 있습니다. raw 데이터(3TB 이상), 변환된 데이터(3TB 이상), 적어도 처리된 데이터(약 500-600GB), 처리 중에 발생할 수 있는 더 많은 캐시 데이터까지 모두 저장할 수 있어야 합니다.

### raw stack_exchange 데이터를 jsonl로 변환

`raw_stackexchange_to_jsonl.py`를 사용하여 raw stack_exchange 데이터를 변환합니다.

이 도구는 [Archive](https://archive.org/download/stackexchange)에서 다운로드한 원시 Stack Exchange 데이터를 여러 jsonl 파일로 변환하는 데 사용됩니다.



```shell
python tools/preprocess/raw_arxiv_stackexchange_to_jsonl.py           \
    --src_dir       <src_dir>      \
    --target_dir    <target_dir>   \
    --topk          <topk>         \
    --num_proc      <num_proc>     \

# 도움말 얻기
python tools/preprocess/raw_stackexchange_to_jsonl.py  --help
```
- `src_dir`: Redpajama처럼 raw Stack Exchange 데이터를 다운로드하면 *.*.com.7z와 같은 파일 이름을 가진 수백 개의 7z 파일이 들어 있는 src 디렉터리를 얻게 됩니다. 이 인수를 이 디렉토리의 경로로 설정하면 됩니다. 또한 이러한 파일을 압축 해제하고 POSTs.xml을 해당 압축된 패키지 이름으로 이름을 바꾸어 해당 디렉터리에 배치해야 합니다. 자세한 내용은 [여기]((https://github.com/togethercomputer/RedPajama-Data/tree/main/data_prep/stack_exchange))를 참조하십시오.
- `target_dir`: 변환된 jsonl 파일을 저장할 결과 디렉토리입니다.
- `topk` (선택 사항): 최대 컨텐츠를 가진 상위 k 사이트를 선택합니다. 기본값은 28입니다.
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.

**참고:** 다운로드, 변환 또는 처리하기 전에 드라이브 공간이 충분히 큰지 확인해야 할 수 있습니다. raw 데이터(100GB 이상), 변환된 데이터(100GB 이상)를 저장할 수 있는지 확인하세요.

### raw Alpaca-CoT 데이터를 jsonl로 변환

`raw_alpaca_cot_merge_add_meta.py`를 사용하여 raw Alpaca-CoT 데이터를 변환합니다.

이 도구는 [HuggingFace](https://huggingface.co/datasets/QingyiSi/Alpaca-CoT)에서 다운로드한 raw Alpaca-Cot 데이터를 여러 jsonl 파일로 변환하는 데 사용됩니다.



```shell
python tools/preprocess/raw_alpaca_cot_merge_add_meta.py       \
    --src_dir           <src_dir>         \
    --target_dir        <target_dir>      \
    --num_proc          <num_proc>

# 도움말 얻기
python tools/preprocess/raw_alpaca_cot_merge_add_meta.py --help
```
- `src_dir`: Alpaca_CoT 데이터를 저장하는 경로로 이 인수를 설정하면 됩니다.
- `target_dir`: 변환된 jsonl 파일을 저장할 결과 디렉토리입니다.
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.

### CSV 또는 TSV 파일 재포맷

이 도구는 일부 필드에 NaN 값이 있을 수 있는 CSV 또는 TSV 파일을 여러 jsonl 파일로 재포맷하는 데 사용됩니다.



```shell
python tools/preprocess/reformat_csv_nan_value.py           \
    --src_dir           <src_dir>         \
    --target_dir        <target_dir>      \
    --suffixes          <suffixes>        \
    --is_tsv            <is_tsv>          \
    --keep_default_na   <keep_default_na> \
    --num_proc          <num_proc>

# 도움말 얻기
python tools/preprocess/reformat_csv_nan_value.py --help
```
- `src_dir`: 이 인수를 `*.csv` 또는 `*.tsv`와 같은 파일 이름이 있는 경로로 설정하면 됩니다.
- `target_dir`: 변환된 jsonl 파일을 저장할 결과 디렉토리입니다.
- `suffixes`: 처리하려는 접미사 유형입니다. 여러 접미사를 처리하려면 `--suffixes '.tsv', '.csv'`와 같이 여러 접미사를 사용합니다.
- `is_tsv`: True이면 sep가 `'\t'`로 설정되고, 그렇지 않으면 기본값으로 `','`로 설정됩니다.
- `keep_default_na`: False이면 문자열이 NaN으로 구문 분석되며, 그렇지 않으면 구문 분석에 기본 NaN 값만 사용됩니다.
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.

### JSONL 파일 재포맷

이 도구는 일부 필드에 NaN 값이 있을 수 있는 JSONL 파일을 재포맷하는 데 사용됩니다.



```shell
python tools/preprocess/reformat_jsonl_nan_value.py           \
    --src_dir           <src_dir>         \
    --target_dir        <target_dir>      \
    --num_proc          <num_proc>

# 도움말 얻기
python tools/preprocess/reformat_jsonl_nan_value.py --help
```
- `src_dir`: 이 인수를 `*.jsonl`과 같은 파일 이름이 있는 경로로 설정하면 됩니다.
- `target_dir`: 변환된 jsonl 파일을 저장할 결과 디렉토리입니다.
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.


### JSONL 파일의 메타 필드 직렬화

일부 JSONL 파일에서 다른 샘플에는 다른 메타 필드가 있을 수 있으며, 동일한 메타 필드 내의 데이터 유형도 다를 수 있습니다. 이로 인해 [HuggingFace Dataset](https://huggingface.co/docs/datasets/index)을 사용하여 데이터셋을 읽을 때 문제가 발생할 수 있습니다. 이 도구는 이러한 JSONL 파일에서 `text_key`를 제외한 모든 메타 필드를 문자열로 직렬화하여 후속 **Data-Modori** 처리를 용이하게 합니다. 데이터셋이 처리된 후에는 일반적으로 [deserialize_meta.py](../postprocess/deserialize_meta.py)를 사용하여 역직렬화해야 합니다.


```shell
python tools/preprocess/serialize_meta.py           \
    --src_dir           <src_dir>         \
    --target_dir        <target_dir>      \
    --text_key          <text_key>        \
    --serialized_key    <serialized_key>  \
    --num_proc          <num_proc>

# 도움말 얻기
python tools/preprocess/serialize_meta.py --help
```
- `src_dir`:  jsonl 파일을 저장하는 경로입니다.
- `target_dir`: 변환된 jsonl 파일을 저장할 결과 디렉토리입니다.
- `text_key`: 직렬화하지 않을 필드에 해당하는 키입니다. 기본값은 'text'입니다.
- `serialized_key`: 직렬화된 정보가 저장된 필드에 해당하는 키입니다. 기본값은 'source_info'입니다.
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.
