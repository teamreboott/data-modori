# 자동 평가 도구킷

모델을 자동으로 평가하고 교육 과정 중 메트릭의 변경 사항을 모니터링합니다.

## 준비

1. 여러 GPU 머신(적어도 2대, 하나는 평가용, 다른 하나는 훈련용)이 필요합니다.

2. 공유 파일 시스템(예: NAS)을 위해 동일한 경로(예: `/mnt/shared`)에 마운트합니다.

3. Data-Modori를 공유 파일 시스템에 설치합니다(예: `/mnt/shared/code/data-modori`).

4. 각 머신에 [thirdparty/README_ko.md](../../thirdparty/README_ko.md)에 따라 Megatron-LM 및 HELM의 서드파티 종속성을 설치합니다.

5. 데이터셋과 토크나이저를 준비하고 Megatron-LM을 사용하여 데이터셋을 mmap 형식으로 전처리합니다(Megatron-LM에 대한 자세한 내용은 [README](../../thirdparty/Megatron-LM/README_ko.md)를 참조하십시오. 공유 파일 시스템에 데이터셋 위치를 지정합니다(예: `/mnt/shared/dataset`).

6. 훈련 머신에서 Megatron-LM을 실행하고 공유 파일 시스템에 체크포인트를 저장합니다(예: `/mnt/shared/checkpoints`).

## 사용법

[evaluator.py](evaluator.py)를 사용하여 HELM 및 OpenAI API로 모델을 자동으로 평가합니다.

```shell
python tools/evaluator.py  \
    --config <config>      \
    --begin-iteration     <begin_iteration>     \
    [--end-iteration      <end_iteration>]      \
    [--iteration-interval <iteration_interval>] \
    [--check-interval <check_interval>]         \
    [--model-type     <model_type>]             \
    [--eval-type      <eval_type>]
```

- `config`: 평가를 실행하는 데 필요한 다양한 설정이 포함된 yaml 파일(자세한 내용은 [Configuration](#configuration) 참조)
- `begin_iteration`: 평가할 첫 번째 체크포인트의 반복
- `end_iteration`: 평가할 마지막 체크포인트의 반복. 설정하지 않으면 훈련 과정을 계속 모니터링하고 생성된 체크포인트를 평가합니다.
- `iteration_interval`: 두 체크포인트 간의 반복 간격, 기본값은 1000 반복
- `check_interval`: 체크 간의 시간 간격, 기본값은 30 분
- `model_type`: 모델 유형, 현재는 megatron 및 huggingface를 지원합니다.
    - `megatron`: Megatron-LM 체크포인트를 평가합니다(기본값)
    - `huggingface`: HuggingFace 모델을 평가하며 현재는 gpt eval 유형만 지원합니다.
- `eval-type`: 실행할 평가 유형, 현재는 `helm` 및 `gpt`를 지원합니다.
    - `helm`: HELM을 사용하여 모델을 평가합니다(기본값). helm 특정 템플릿 파일을 수정하여 실행할 벤치마크를 변경할 수 있습니다.
    - `gpt`: OpenAI API를 사용하여 모델을 평가합니다. 자세한 내용은 [gpt_eval/README_ko.md](gpt_eval/README_ko.md)에서 찾을 수 있습니다.

> e.g.,
> ```shell
> python evaluator.py --config <config_file> --begin-iteration 2000 --iteration-interval 1000 --check-interval 10
> ```
> 이 명령은 2000 반복부터 시작하여 1000 반복마다 Megatron-LM 체크포인트를 HELM을 사용하여 평가하고, 10 분마다 새로운 체크포인트가 지정된 조건을 충족하는지 확인합니다.

[evaluator.py](evaluator.py)를 실행한 후에는 [recorder/wandb_writer.py](recorder/wandb_writer.py)를 사용하여 평가 결과를 시각화할 수 있습니다. 자세한 내용은 [recorder/README_ko.md](recorder/README_ko.md)에서 확인할 수 있습니다.

## 구성

config_file의 형식은 다음과 같습니다.

```yaml
auto_eval:
  project_name: <str> # 프로젝트 이름
  model_name: <str>   # 모델 이름
  cache_dir: <str>    # 캐시 디렉토리 경로
  megatron:
    process_num: <int>     # Megatron 실행 프로세스 수
    megatron_home: <str>   # Megatron-LM 루트 디렉토리
    checkpoint_path: <str> # 체크포인트 디렉토리 경로
    tokenizer_type: <str>  # 현재 gpt2 또는 sentencepiece을 지원
    vocab_path: <str>      # gpt2 토크나이저 유형에 대한 구성, 어휘 파일 경로
    merge_path: <str>      # gpt2 토크나이저 유형에 대한 구성, 병합 파일 경로
    tokenizer_path: <str>  # sentencepiece 토크나이저 유형에 대한 구성, 모델 파일 경로
    max_tokens: <int>      # 추론에서 생성할 최대 토큰 수
    token_per_iteration: <float> # 이터레이션당 십억 개의 토큰
  helm:
    helm_spec_template_path: <str> # helm 스펙 템플릿 파일 경로, 기본값은 tools/evaluator/config/helm_spec_template.conf
    helm_output_path: <str>  # helm 출력 디렉토리 경로
    helm_env_name: <str>     # helm conda 환경 이름
  gpt_evaluation:
    # openai 구성
    openai_api_key: <str>       # API 키
    openai_organization: <str>  # 조직
    # 파일 구성
    question_file: <str>  # 기본값은 tools/evaluator/gpt_eval/config/question.jsonl
    baseline_file: <str>  # 기본값은 tools/evaluator/gpt_eval/answer/openai/gpt-3.5-turbo.jsonl
    prompt_file: <str >   # 기본값은 tools/evaluator/gpt_eval/config/prompt.jsonl
    reviewer_file: <str>  # 기본값은 tools/evaluator/gpt_eval/config/reviewer.jsonl
    answer_file: <str>    # 생성된 답변 파일 경로
    result_file: <str>    # 생성된 리뷰 파일 경로
```
