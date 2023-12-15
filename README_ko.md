[English](README.md) | 한국어

# Data-Modori: 한국어용 LMOps 도구

<div align="center">
  <img src="https://github.com/teamreboott/data-modori/blob/main/docs/imgs/buri_heart.png?raw=true" width="300"/>
  <div>&nbsp;</div>
  <div align="center">
    <b><font size="5">TEAMREBOOTT website </font></b>
    <sup>
      <a href="https://reboott.ai">
        <i><font size="4">HOT</font></i>
      </a>
    </sup>
    &nbsp;&nbsp;&nbsp;&nbsp;
    <b><font size="5">TeamAR platform</font></b>
    <sup>
      <a href="https://askyour.trade">
        <i><font size="4">TRY IT OUT</font></i>
      </a>
    </sup>
  </div>
  <div>&nbsp;</div>


![](https://img.shields.io/badge/license-Apache--2.0-ff655b.svg)
![](https://img.shields.io/badge/language-Python-b44dff.svg)
[![Contributing](https://img.shields.io/badge/Contribution-welcome-5bc4ff.svg)](docs/DeveloperGuide_ko.md)

[📘문서](#문서) |
[🛠️설치방법](#설치방법) |
[🤔이슈보고](https://github.com/teamreboott/data-modori/issues/new/choose)

</div>

Data-Modori는 수집한 데이터를 이용해 다양한 가능성을 제공하는 창의적이고 진보적입니다. 우리는 데이터의 모든 조각들을 하나로 조립하여 원하는 정보의 세계로 여러분을 초대합니다.

- 데이터 통합: 다양한 소스로부터 데이터를 수집하여 하나의 중앙 허브로 통합하여 편리하게 사용할 수 있습니다.
- 유연한 분석: 고급 분석 도구를 활용하여 데이터를 심층적으로 분석하고 새로운 인사이트와 관점을 얻을 수 있습니다.
- 맞춤형 결과: 요구 사항에 따라 데이터를 구성하고 표시하여 맞춤형 결과를 제공합니다.
- 사용자 친화적인 인터페이스: 직관적이고 사용하기 쉬운 인터페이스를 통해 사용자는 고급 지식 없이도 데이터의 힘을 활용할 수 있습니다.

----

목차
=================
- [Data-Modori: 한국어용 LMOps 도구](#data-modori-한국어용-lmops-도구)
- [목차](#목차)
  - [설치방법](#설치방법)
  - [데이터 전처리](#데이터-전처리)
  - [데이터 분석](#데이터-분석)
  - [데이터 시각화](#데이터-시각화)
  - [설정 파일 구성](#설정-파일-구성)
  - [문서](#문서)
  - [License](#license)
  - [기여하기](#기여하기)
  - [감사한분들](#감사한분들)
  - [참고문헌](#참고문헌)

### 설치방법

- **Github**에서 소스 코드 가져오기
```bash
git clone https://github.com/teamreboott/data-modori
cd data-modori
```

- 다음 명령을 실행하여 **data-modori**에서 필요한 모듈을 설치합니다:
```bash
pip install -r environments/combined_requirements.txt
```

### 데이터 전처리

- `process_data.py`와 config 파일을 사용해 데이터셋을 처리합니다.

```bash
python tools/process_data.py --config configs/process.yaml
```

- **참고:** 로컬에 저장되지 않은 third-party models 또는 리소스가 필요한 일부 연산자의 경우, 리소스를 다운하기 위해 처음 실행할 때 시간이 걸릴 수 있습니다.
기본 다운로드 캐시 디렉터리는 `~/.cache/data_modori`에 위치합니다. 다른 디렉토리로 캐시 위치를 변경하려면 셸 환경 변수 `DATA_MODORI_CACHE_HOME`을 다른 디렉터리로 설정하고
`DATA_MODORI_MODELS_CACHE` 또는 `DATA_MODORI_ASSETS_CACHE`도 동일한 방식으로 변경할 수 있습니다:

```bash
# cache home
export DATA_MODORI_CACHE_HOME="/path/to/another/directory"
# cache models
export DATA_MODORI_MODELS_CACHE="/path/to/another/directory/models"
# cache assets
export DATA_MODORI_ASSETS_CACHE="/path/to/another/directory/assets"
```

### 데이터 분석

- `analyze_data.py`와 config 파일을 사용해 데이터셋을 분석합니다.

```bash
python tools/analyze_data.py --config configs/analyser.yaml
```

- **참고:** `analyze_data.py`는 Filter ops의 통계만 계산합니다. 따라서 Mapper or Deduplicator ops는 분석 프로세스에서 무시됩니다.

### 데이터 시각화

- `app.py` 를 실행하여 브라우저에서 데이터셋을 시각화합니다.

```bash
streamlit run app.py
```

### 설정 파일 구성

- 설정 파일은 전역 인수 및 데이터 처리를 위한 연산자 목록을 지정합니다. 다음을 설정해야 합니다:
  - 전역 인수: 입력/출력 데이터셋 경로, 작업자 수 등
  - 연산자 목록: 데이터셋을 처리하는 데 사용되는 연산자와 해당 인수 목록
- 다음 방법으로 자체 설정 파일을 작성할 수 있습니다:
  - ➖: 우리의 예제 설정 파일 config_all.yaml을 수정합니다. 이 파일에는 모든 연산자와 기본 인수가 포함되어 있습니다. 사용하지 않을 연산자를 제거하고 일부 연산자의 인수를 수정하면 됩니다.
  - ➕: 예제 설정 파일 [`config_all.yaml`](configs/config_all.yaml), [연산자 문서](docs/Operators_ko.md), 그리고 [개발자를 위한 사용법 가이드](docs/DeveloperGuide_ko.md#build-your-own-configs)를 참조하여 처음부터 자체 설정 파일을 작성합니다.
- yaml 파일 외에도 명령 줄에서 하나의 (여러 개 중의 하나) 매개변수만 지정하여 yaml 파일의 값을 무시하고 변경할 수 있습니다.

```bash
python xxx.py --config configs/process.yaml --language_id_score_filter.lang=ko 
```
    
```bash
# 데이터 셋에 대한 프로세스 구성 예제

# 전역변수
project_name: 'demo-process'
dataset_path: './data/test.json'  # 데이터 세트 디렉토리 또는 파일 경로
export_path: './output/test.jsonl'

np: 4  # 데이터 셋을 처리할 프로세스 개수
text_keys: 'content'

# 프로세스 스케줄
# 인수가 포함된 여러 프로세스 연산자 목록
process:
  - language_id_score_filter:
      lang: 'en'
```

## License
**Data-Modori**는 Apache 라이선스 2.0에 따라 배포됩니다.

## 기여하기
저희는 빠르게 발전하는 분야에 속해 있으며 새로운 기능, 버그 수정, 더 나은 문서를 기능, 버그 수정 및 더 나은 문서에 대한 기여를 크게 환영합니다. 
[개발자를 위한 사용법 가이드](docs/DeveloperGuide_ko.md)를 참조하세요.

## 감사한분들
**Data-Modori**는 다양한 LLM 제품 및 연구 이니셔티브에서 사용됩니다,
다양한 LLM 제품 및 연구 이니셔티브에 사용됩니다, 
무역용 AUT, 업무용 AUW 등 다양한 산업 LLM에 사용됩니다. 

협업을 위한 여러분의 더 많은 경험, 제안, 토론을 기다리겠습니다!

**Data-Modori**는 다음과 같은 여러 커뮤니티 프로젝트에 감사를 표하고 참조합니다. 
[data-juicer](https://github.com/alibaba/data-juicer), [Huggingface-Datasets](https://github.com/huggingface/datasets), [Bloom](https://huggingface.co/bigscience/bloom), [Pile](https://huggingface.co/datasets/EleutherAI/pile), [Megatron-LM](https://github.com/NVIDIA/Megatron-LM), [DeepSpeed](https://www.deepspeed.ai/), [Arrow](https://github.com/apache/arrow), [Ray](https://github.com/ray-project/ray), [Beam](https://github.com/apache/beam),  [LM-Harness](https://github.com/EleutherAI/lm-evaluation-harness), [HELM](https://github.com/stanford-crfm/helm), ....

## 참고문헌
저희의 연구가 귀사의 연구나 개발에 도움이 된다면 다음 [논문](https://arxiv.org/abs/2309.02033)을 인용해 주시기 바랍니다.
```
@misc{chen2023datajuicer,
title={Data-Juicer: A One-Stop Data Processing System for Large Language Models},
author={Daoyuan Chen and Yilun Huang and Zhijian Ma and Hesen Chen and Xuchen Pan and Ce Ge and Dawei Gao and Yuexiang Xie and Zhaoyang Liu and Jinyang Gao and Yaliang Li and Bolin Ding and Jingren Zhou},
year={2023},
eprint={2309.02033},
archivePrefix={arXiv},
primaryClass={cs.LG}
}
```
