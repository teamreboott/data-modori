# Data Juicer

해당 페이지는 개발 중입니다.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Data Processing](#data-processing)
- [Data Analysis](#data-analysis)
- [Data Visualization](#data-visualization)
- [Build Up Config Files](#build-up-config-files)
- [Example Command](#example-command)

## Installation

```bash
# Git에서 소스 코드 가져오기
git clone https://github.com/teamreboott/data-juicer
cd data-juicer

# 가상환경 설정 및 의존성 설치
pip install -v -e .[all]

# 또는 선택적 의존성 설치
pip install -v -e .[tools]  # 도구에 필요한 의존성만 설치

# 선택적으로 버전 확인
import data_juicer as dj
print(dj.__version__)

# pip로 설치하기 (제한된 기능 포함)
# 설치 명령어
pip install py-data-juicer
```

# Usage
Brief description of how to use your project.

# Data Processing
## Tool Usage
```bash
python tools/process_data.py --config configs/process.yaml

dj-process --config configs/process.yaml
```

Notes
- 몇몇 작업에서는 로컬에 저장되지 않은 서드파티 모델이나 리소스가 필요할 수 있습니다.
- 처음 실행 시 다운로드에 시간이 걸릴 수 있으며, 캐시 디렉토리는 `~/.cache/data_juicer`에 위치합니다.

# Data Analysis
## Tool Usage
```bash
python tools/analyze_data.py --config configs/analyser.yaml

dj-analyze --config configs/analyser.yaml
```

Notes
- Analyser는 Filter 연산의 통계만 계산하며, 추가적인 Mapper나 Deduplicator 연산은 무시됩니다.

# Data Visualization
## Tool Usage
```bash
streamlit run app.py
```
Note
- 이 기능은 소스 설치에서만 사용 가능합니다.

# Build Up Config Files
## Config File Example
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
## Example Command
```bash
python xxx.py --config configs/process.yaml --language_id_score_filter.lang=en
```
Note
- 프로젝트에 맞게 이 템플릿을 수정하고 확장하십시오.