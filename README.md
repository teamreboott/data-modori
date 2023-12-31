English | [한국어](README_ko.md)

# Data-Modori: LMOps Tool for Korean

<div align="center">
  <img src="https://github.com/teamreboott/data-modori/blob/main/docs/imgs/buri_heart.png?raw=true" width="300"/>
  <div>&nbsp;</div>
  <div align="center">
    <b><font size="5">TEAMREBOOTT Inc. </font></b>
    <sup>
      <a href="https://reboott.ai">
        <i><font size="4">HOT</font></i>
      </a>
    </sup>
    &nbsp;&nbsp;&nbsp;&nbsp;
  </div>
  <div>&nbsp;</div>


![](https://img.shields.io/badge/license-Apache--2.0-ff655b.svg)
![](https://img.shields.io/badge/language-Python-b44dff.svg)
[![Contributing](https://img.shields.io/badge/Contribution-welcome-5bc4ff.svg)](docs/DeveloperGuide.md)

[📘Documentation](#documentation) |
[🛠️Installation](#installation) |
[🤔Reporting Issues](https://github.com/teamreboott/data-modori/issues/new/choose)

</div>

**LMOps** is a complex and challenging field, but it plays a pivotal role in the successful deployment and management of large language models.  
**Data-Modori** is an unified platform that guides you into the realm of LLM, offering diverse possibilities by analyzing useful information from various sources 🌐. 
We gather all the puzzle pieces of the developing process of LLM, assemble them into one, and invite you into the world of the information you desire.

- 🛠️ **Flexible Analysis**: Utilize advanced analysis tools to delve into your data for Korean languages, gaining new insights and perspectives.
- 📊 **Customized Results**: Organize and present data according to your requirements, delivering tailored results.
- 🖥️ **User-Friendly Interface**: An intuitive and easy-to-use interface allows users to harness the power of data without requiring advanced knowledge.
- 🤖 **Easy-to-Learn**: We provide an intuitive codes, including finetuning and auto-eval codes fot LLMs.

----

Table of Contents
=================
- [Data-Modori: LMOps Tool for Korean](#data-modori-lmops-tool-for-korean)
- [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Data Processing](#data-processing)
  - [Data Analysis](#data-analysis)
  - [Data Visualization](#data-visualization)
  - [Build Up Config Files for Preprocessing](#build-up-config-files)
  - [Supervised Fine-Tuning (SFT)](tools/finetuning/README.md)
  - [Direct Preference Optimization (DPO)](tools/finetuning/README.md)
  - [Korean Language Model Evaluation Harness](tools/evaluator/README.md)
  - [Documentation](#documentation)
  - [License](#license)
  - [Contributing](#contributing)
  - [Acknowledgement](#acknowledgement)


### Prerequisites

- Recommend Python==3.8
- gcc >= 5 (at least C++14 support)


### ⚙️ Installation

- Get source code from **Github**
```bash
git clone https://github.com/teamreboott/data-modori
cd data-modori
```

- Run the following command to install the required modules from **data-modori**:
```bash
pip install -r environments/combined_requirements.txt
```

### 📊 Data Processing

**Data-Modori** provides a variety of [operators](docs/Operators.md)!

- Run `process_data.py` tool with your config as the argument to process your dataset.

```bash
python tools/process_data.py --config configs/process.yaml
```

- **Note:** For some operators that involve third-party models or resources which are not stored locally on your computer, it might be slow for the first running because these ops need to download corresponding resources into a directory first.
The default download cache directory is `~/.cache/data_modori`. Change the cache location by setting the shell environment variable, `DATA_MODORI_CACHE_HOME` to another directory, and you can also change `DATA_MODORI_MODELS_CACHE` or `DATA_MODORI_ASSETS_CACHE` in the same way:

```bash
# cache home
export DATA_MODORI_CACHE_HOME="/path/to/another/directory"
# cache models
export DATA_MODORI_MODELS_CACHE="/path/to/another/directory/models"
# cache assets
export DATA_MODORI_ASSETS_CACHE="/path/to/another/directory/assets"
```

### 🔍 Data Analysis

- Run `analyze_data.py` tool with your config as the argument to analyse your dataset.

```bash
python tools/analyze_data.py --config configs/analyser.yaml
```

- **Note:** Analyser only compute stats of Filter ops. So extra Mapper or Deduplicator ops will be ignored in the analysis process.

### 📈 Data Visualization

- Run `app.py` tool to visualize your dataset in your browser.

```bash
streamlit run app.py
```

![Example of App](docs/imgs/streamlit_ex.png "Streamlit App")


### 🏗️ Build Up Config Files

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
      lang: 'ko'
```

## 📖 Documentation

- [Overview](README.md)
- [Operators](docs/Operators.md)
- [Configs](configs/README.md)
- [Developer Guide](docs/DeveloperGuide.md)

## 🔐 License
**Data-Modori** is released under Apache License 2.0.

## 🤝 Contributing
We are in a rapidly developing field and greatly welcome contributions of new 
features, bug fixes and better documentations. Please refer to [How-to Guide for Developers](docs/DeveloperGuide.md).

## 🙏  Acknowledgement
**Data-Modori** is used across various LLM projects and research initiatives,
including industrial LLMs.
We look forward to more of your experience, suggestions and discussions for collaboration!

We thank and refers to several community projects, such as 
[data-juicer](https://github.com/alibaba/data-juicer), [KoBERT](https://github.com/SKTBrain/KoBERT/tree/master), [komt](https://github.com/davidkim205/komt), [ko-lm-evaluation-harness](https://github.com/Beomi/ko-lm-evaluation-harness), [Huggingface-Datasets](https://github.com/huggingface/datasets), [Bloom](https://huggingface.co/bigscience/bloom), [Pile](https://huggingface.co/datasets/EleutherAI/pile), [Megatron-LM](https://github.com/NVIDIA/Megatron-LM), [DeepSpeed](https://www.deepspeed.ai/), [Arrow](https://github.com/apache/arrow), [Ray](https://github.com/ray-project/ray), [Beam](https://github.com/apache/beam),  [LM-Harness](https://github.com/EleutherAI/lm-evaluation-harness), [HELM](https://github.com/stanford-crfm/helm), ....

