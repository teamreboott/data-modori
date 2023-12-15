# 후처리 도구

이 폴더에는 **Data-Modori**를 사용하여 처리된 데이터셋을 추가로 처리하기 위한 몇 가지 후처리 스크립트가 포함되어 있습니다.

## 사용법

### 데이터셋 토큰 수 세기

카운트 [count_token.py](count_token.py)를 사용하여 데이터셋의 토큰 수를 세십시오.

```shell
python tools/postprocess/count_token.py        \
    --data_path            <data_path>         \
    --text_keys            <text_keys>         \
    --tokenizer_method     <tokenizer_method>  \
    --num_proc             <num_proc>
    
# 도움말 얻기
python tools/postprocess/count_token.py --help
```

- `data_path`: 입력 데이터셋의 경로. 현재는 `jsonl`만 지원합니다.
- `text_keys`: 토큰 수에 고려될 필드 키입니다.
- `tokenizer_method`: Hugging Face 토크나이저의 이름입니다.
- `num_proc`: 토큰을 세는 데 사용할 프로세스의 수입니다.

### 선택적 가중치를 사용하여 여러 데이터셋 섞기

[data_mixture.py](data_mixture.py)를 사용하여 여러 데이터셋을 혼합합니다.

이 스크립트는 각 데이터셋에서 샘플을 무작위로 선택하고 이러한 샘플을 섞어 새 데이터셋으로 내보냅니다.

```shell
python tools/postprocess/data_mixture.py        \
    --data_path             <data_path>         \
    --export_path           <export_path>       \
    --export_shard_size     <export_shard_size> \
    --num_proc              <num_proc>

# 도움말 얻기
python tools/postprocess/data_mixture.py  --help
```

- `data_path`: 데이터셋 파일 또는 데이터셋 파일 목록 또는 둘 다의 목록 및 가중치. 설정되지 않으면 기본값으로 1.0입니다.
- `export_path`: 혼합된 데이터셋을 내보낼 데이터셋 파일 이름, `json` / `jsonl` / `parquet`을 지원합니다.
- `export_shard_size`: 바이트 단위의 데이터셋 파일 크기입니다. 설정되지 않으면 혼합된 데이터셋은 하나의 파일에 내보내집니다.
- `num_proc`: 데이터셋을 로드하고 내보내기 위한 프로세스 수입니다.

- 예: `python tools/postprocess/data_mixture.py  --data_path  <w1> ds.jsonl <w2> ds_dir <w3> ds_file.json`

**참고:** 모든 데이터셋은 동일한 메타 필드를 가져야 하므로 [HuggingFace Datasets](https://huggingface.co/docs/datasets/index)를 사용하여 기능을 정렬할 수 있습니다.

### jsonl 파일에서 메타 필드 역직렬화

이 도구는 일반적으로 [serialize_meta.py](../preprocess/serialize_meta.py)와 함께 사용되어 특정 필드를 원래 형식으로 역직렬화합니다.

```shell
python tools/postprocess/deserialize_meta.py           \
    --src_dir           <src_dir>         \
    --target_dir        <target_dir>      \
    --serialized_key    <serialized_key>  \
    --num_proc          <num_proc>

# 도움말 얻기
python tools/postprocess/deserialize_meta.py --help
```
- `src_dir`: jsonl 파일을 저장할 경로입니다.
- `target_dir`: 변환된 jsonl 파일을 저장할 경로입니다.
- `serialized_key`: 역직렬화할 필드에 해당하는 키입니다. 기본값은 'source_info'입니다.
- `num_proc` (선택 사항): 프로세스 워커 수입니다. 기본값은 1입니다.

**참고:** 역직렬화 후 원래 파일의 모든 직렬화된 필드는 `'serialized_key'`에 배치됩니다. 이는 **Data-Modori** 처리 후 생성된 필드가 원래 메타 필드와 충돌하지 않도록하기 위한 것입니다.
