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

### Installation

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

### Data Processing

- Run `process_data.py` tool with your config as the argument to process your dataset.

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

### Data Analysis

- Run `analyze_data.py` tool with your config as the argument to analyse your dataset.

```bash
python tools/analyze_data.py --config configs/analyser.yaml
```

- **Note:** Analyser only compute stats of Filter ops. So extra Mapper or Deduplicator ops will be ignored in the analysis process.

### Data Visualization

- Run `app.py` tool to visualize your dataset in your browser.
- **Note**: only available for installation from source.

```bash
streamlit run app.py
```

### Build Up Config Files

- Config files specify some global arguments, and an operator list for the
  data process. You need to set:
  - Global arguments: input/output dataset path, number of workers, etc.
  - Operator list: list operators with their arguments used to process the dataset.
- You can build up your own config files by:
  - ➖：Modify from our example config file [`config_all.yaml`](configs/config_all.yaml) which includes **all** ops and default
    arguments. You just need to **remove** ops that you won't use and refine
    some arguments of ops.
  - ➕：Build up your own config files **from scratch**. You can refer our
    example config file [`config_all.yaml`](configs/config_all.yaml), [op documents](docs/Operators.md), and advanced [Build-Up Guide for developers](docs/DeveloperGuide.md#build-your-own-configs).
  - Besides the yaml files, you also have the flexibility to specify just
    one (of several) parameters on the command line, which will override
    the values in yaml files.
    
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
