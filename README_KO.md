[English](README.md) | 한국어

# Data-Modori: 데이터 세계의 새로운 지평을 열다

<div align="center">
  <img src="https://github.com/teamreboott/data-juicer/assets/40276516/86ec78ca-fb84-4367-a7d5-b67220114e39" width="300"/>
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
[![Contributing](https://img.shields.io/badge/Contribution-welcome-5bc4ff.svg)](docs/DeveloperGuide.md)

<!-- [![pypi version](https://img.shields.io/pypi/v/py-data-juicer?logo=pypi&color=ffb84d)](https://pypi.org/project/py-data-juicer)
[![Docker version](https://img.shields.io/docker/v/datajuicer/data-juicer?logo=docker&label=Docker&color=0100FF)](https://hub.docker.com/r/datajuicer/data-juicer)
[![Document_List](https://img.shields.io/badge/Docs-English-FAED7D?logo=Markdown)](README.md#documentation) -->

[📘문서]() |
[🛠️설치]() |
[🤔문제]()

</div>

Data-Modori는 수집한 데이터를 이용해 다양한 가능성을 제공하는 창의적이고 진보적입니다. 우리는 데이터의 모든 조각들을 하나로 조립하여 원하는 정보의 세계로 여러분을 초대합니다.

- 데이터 통합: 다양한 소스로부터 데이터를 수집하여 하나의 중앙 허브로 통합하여 편리하게 사용할 수 있습니다.
- 유연한 분석: 고급 분석 도구를 활용하여 데이터를 심층적으로 분석하고 새로운 인사이트와 관점을 얻을 수 있습니다.
- 맞춤형 결과: 요구 사항에 따라 데이터를 구성하고 표시하여 맞춤형 결과를 제공합니다.
- 사용자 친화적인 인터페이스: 직관적이고 사용하기 쉬운 인터페이스를 통해 사용자는 고급 지식 없이도 데이터의 힘을 활용할 수 있습니다.

----

## Table of Contents

- [설치](#installation)
- [데이터 전처리](#data-processing)
- [데이터 분석](#data-analysis)
- [데이터 시각화](#data-visualization)
- [Config 파일 구축](#build-up-config-files)

### 설치

- **Github**에서 소스 코드 가져오기
```bash
git clone https://github.com/teamreboott/data-juicer
cd data-juicer
```

- 다음 명령을 실행하여 최신 Data-Modori 버전을 설치합니다:
```bash
pip install -v -e .
```

- 일부 OP는 너무 크거나 플랫폼 호환성이 낮은 타사 라이브러리에 의존합니다. 필요에 따라 선택적 종속성을 설치할 수 있습니다:
```bash
pip install -v -e .  # install a minimal dependencies, which support the basic functions
pip install -v -e .[tools] # install a subset of tools dependencies
```

- The dependency options are listed below:

| Tag          | Description                                                           |
|--------------|-----------------------------------------------------------------------|
| `.` or `.[mini]` | 기본 Data-Modori를 위한 최소한의 종속성을 설치합니다.                                   |
| `.[all]`       | 모든 선택적 종속성을 설치합니다 (최소한의 종속성 및 아래의 모든 종속성).                            |
| `.[sci]`       | 모든 OPs에 대한 모든 종속성을 설치합니다.                                             |
| `.[dist]`      | 분산 데이터 처리를 위한 종속성을 설치합니다. (실험적인 기능)                                   |
| `.[dev]`       | 패키지를 개발자로서 개발하는 데 필요한 종속성을 설치합니다.                                     |
| `.[tools]`     | 품질 분류기와 같은 특수 도구를 위한 종속성을 설치합니다. |

### 데이터 전처리

- `process_data.py` 도구와 config 파일을 사용하여 데이터셋을 처리합니다.

```bash
python tools/process_data.py --config configs/process.yaml
```

- **참고:** 로컬에 저장되지 않은 third-party models 또는 리소스가 필요한 일부 연산자의 경우, 리소스를 다운하기 위해 처음 실행할 때 시간이 걸릴 수 있습니다.
기본 다운로드 캐시 디렉터리는 ~/.cache/data_juicer에 위치합니다. 다른 디렉토리로 캐시 위치를 변경하려면 셸 환경 변수 DATA_JUICER_CACHE_HOME을 다른 디렉터리로 설정하고
DATA_JUICER_MODELS_CACHE 또는 DATA_JUICER_ASSETS_CACHE도 동일한 방식으로 변경할 수 있습니다.

- **Note:** For some operators that involve third-party models or resources which are not stored locally on your computer, it might be slow for the first running because these ops need to download corresponding resources into a directory first.
The default download cache directory is `~/.cache/data_juicer`. Change the cache location by setting the shell environment variable, `DATA_JUICER_CACHE_HOME` to another directory, and you can also change `DATA_JUICER_MODELS_CACHE` or `DATA_JUICER_ASSETS_CACHE` in the same way:

```bash
# cache home
export DATA_JUICER_CACHE_HOME="/path/to/another/directory"
# cache models
export DATA_JUICER_MODELS_CACHE="/path/to/another/directory/models"
# cache assets
export DATA_JUICER_ASSETS_CACHE="/path/to/another/directory/assets"
```

### 데이터 분석

- `analyze_data.py` 도구와 config 파일을 사용하여 데이터셋을 분석합니다.

```bash
python tools/analyze_data.py --config configs/analyser.yaml
```

- **참고:** 분석기는 Filter ops의 통계만 계산합니다. 따라서 Mapper or Deduplicator ops는 분석 프로세스에서 무시됩니다.

### 데이터 시각화

- `app.py` 를 실행하여 브라우저에서 데이터셋을 시각화합니다.

```bash
streamlit run app.py
```

### Config 파일 구축

- Config 파일은 전역 인수와 데이터 프로세스를 위해 사용되는 연산자 목록을 지정합니다.
  - 전역 인수: 입력/출력 데이터셋 경로, 워커 수 등을 설정합니다.
  - 연산자 목록: 데이터셋을 처리하는 데 사용되는 연산자와 해당 인수를 나열합니다.
- 다음 중 하나로 자체 구성 파일을 작성할 수 있습니다.
  - ➖: config_all.yaml 예제 구성 파일에서 수정 (사용하지 않을 연산자를 제거하고 인수를 정리하세요).
  - ➕: 처음부터 자체 구성 파일 작성. 예제 구성 파일 [`config_all.yaml`](configs/config_all.yaml), [op documents](docs/Operators.md) 및 [Build-Up Guide for developers](docs/DeveloperGuide.md#build-your-own-configs)을 참조할 수 있습니다.
  - yaml 파일 외에도 명령 줄에서 파라미터 하나만 지정하여 yaml 파일의 값을 무시하고 변경할 수 있습니다.
```bash
python xxx.py --config configs/process.yaml --language_id_score_filter.lang=ko 
```
    
```bash
# Process config example for dataset

# global parameters
project_name: 'demo-process'
dataset_path: './data/test.json'  # path to your dataset directory or file
export_path: './output/test.jsonl'

np: 4  # number of subprocess to process your dataset
text_keys: 'content'

# process schedule
# a list of several process operators with their arguments
process:
  - language_id_score_filter:
      lang: 'en'
```

## License
Data-Modori is released under Apache License 2.0.

## Contributing
We are in a rapidly developing field and greatly welcome contributions of new 
features, bug fixes and better documentations. Please refer to[How-to Guide for Developers](docs/DeveloperGuide.md).

## Acknowledgement
Data-Modori is used across various LLM products and research initiatives,
including industrial LLMs from Teamreboott AI TEAM(AR), 
such as AUT for trade and AUW for work. 

We look forward to more of your experience, suggestions and discussions for collaboration!

Data-Modori thanks and refers to several community projects, such as 
[data-juicer](https://github.com/alibaba/data-juicer), [Huggingface-Datasets](https://github.com/huggingface/datasets), [Bloom](https://huggingface.co/bigscience/bloom), [RedPajama](https://github.com/togethercomputer/RedPajama-Data), [Pile](https://huggingface.co/datasets/EleutherAI/pile), [Alpaca-Cot](https://huggingface.co/datasets/QingyiSi/Alpaca-CoT), [Megatron-LM](https://github.com/NVIDIA/Megatron-LM), [DeepSpeed](https://www.deepspeed.ai/), [Arrow](https://github.com/apache/arrow), [Ray](https://github.com/ray-project/ray), [Beam](https://github.com/apache/beam),  [LM-Harness](https://github.com/EleutherAI/lm-evaluation-harness), [HELM](https://github.com/stanford-crfm/helm), ....

## References
If you find our work useful for your research or development, please kindly cite the following [paper](https://arxiv.org/abs/2309.02033).
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