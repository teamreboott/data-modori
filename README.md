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


[![platform](https://img.shields.io/badge/platform-Linux%7CWindows%7CmacOS-blue&color=498bdf)]()
![](https://img.shields.io/badge/language-Python-b44dff.svg)
![](https://img.shields.io/badge/license-Apache--2.0-ff655b.svg)
[![Contributing](https://img.shields.io/badge/Contribution-welcome-5bc4ff.svg)](docs/DeveloperGuide.md)

[![pypi version](https://img.shields.io/pypi/v/py-data-juicer?logo=pypi&color=ffb84d)](https://pypi.org/project/py-data-juicer)
[![Docker version](https://img.shields.io/docker/v/datajuicer/data-juicer?logo=docker&label=Docker&color=0100FF)](https://hub.docker.com/r/datajuicer/data-juicer)
[![Document_List](https://img.shields.io/badge/Docs-English-FAED7D?logo=Markdown)](README.md#documentation)

[📘Documentation]() |
[🛠️Installation]() |
[🤔Reporting Issues]()

</div>

<div align="center">

English | [한국어](README_KO.md)

</div>

## Table of Contents

- [Installation](#installation)
- [Data Processing](#data-processing)
- [Data Analysis](#data-analysis)
- [Data Visualization](#data-visualization)
- [Build Up Config Files](#build-up-config-files)
- [Example Command](#example-command)

# Installation

- Get source code from **Github**
```bash
git clone https://github.com/teamreboott/data-juicer
cd data-juicer
```

- Run the following commands to install the latest basic data_juicer version in editable mode:
```bash
pip install -v -e .
```

- Some OPs rely on some other too large or low-platform-compatibility third-party libraries. You can install optional dependencies as needed:
```bash
pip install -v -e .  # install a minimal dependencies, which support the basic functions
pip install -v -e .[tools] # install a subset of tools dependencies
```

- The dependency options are listed below:

| Tag          | Description                                                                                  |
|--------------|----------------------------------------------------------------------------------------------|
| `.` or `.[mini]` | Install minimal dependencies for basic Data-Juicer.                                          |
| `.[all]`       | Install all optional dependencies (including minimal dependencies and all of the following). |
| `.[sci]`       | Install all dependencies for all OPs.                                                        |
| `.[dist]`      | Install dependencies for distributed data processing. (Experimental)                         |
| `.[dev]`       | Install dependencies for developing the package as contributors.                             |
| `.[tools]`     | Install dependencies for dedicated tools, such as quality classifiers.                       |

- If you check the version you have installed
```bash
import data_juicer as dj
print(dj.__version__)
```

# Data Processing

- Run `process_data.py` tool with your config as the argument to process your dataset.

## Tool Usage
```bash
python tools/process_data.py --config configs/process.yaml
```

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
