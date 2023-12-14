import datasets
import glob
import os
import json
import unicodedata
from tqdm import tqdm


PT = "[INST] {} [/INST]"


def KorquadChat(path:str = "heegyu/korquad-chat-v1", cache_dir:str = "./cache"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset['train']['text']
    recon_dataset = []
    for src in sources:
        try:
            prompt = src.split("<bot>")[0].replace("<sys>", "").replace("<usr>", "\n").strip()
            answer = src.split("<bot>")[1].split("<usr>")[0].replace("<bot>", "").strip()
            d = {"instruction": PT.format(prompt), "output": answer}
            recon_dataset.append(d)
        except:
            continue
    return recon_dataset


def NamuWiki(path:str = "psymon/namuwiki_alpaca_dataset", cache_dir:str = "./cache"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset['train']
    recon_dataset = []
    for src in sources:
        output = src['output']
        ins = src['instruction']
        d = {"instruction": PT.format(ins), "output": output}
        recon_dataset.append(d)
    return recon_dataset


def KOpenPlatypus(path:str = "kyujinpy/KOpen-platypus", cache_dir:str = "./cache", data_type:str = "train"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset[data_type]
    recon_dataset = []
    for src in sources:
        output = src['output']
        ins = src['instruction']
        inp = src['input']
        if inp is not None:
            ins = ins + "\n" + inp

        d = {"instruction": PT.format(ins), "output": output}
        recon_dataset.append(d)
    return recon_dataset


def KoCOT(path:str = "kyujinpy/KoCoT_2000", cache_dir:str = "./cache"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset['train']
    recon_dataset = []
    for src in sources:
        output = src['rationale']
        ins = src['source']

        d = {"instruction": PT.format(ins), "output": output}
        recon_dataset.append(d)
    return recon_dataset


def OpenOrca(path:str = "Open-Orca/OpenOrca", cache_dir:str = "./cache"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset['train']
    recon_dataset = []
    for src in sources:
        system = src['system_prompt']
        output = src['response']
        ins = src['question']
        
        if system is not None:
            ins = system + "\n\n" + ins

        d = {"instruction": PT.format(ins), "output": output}
        recon_dataset.append(d)
    return recon_dataset


def NoRobots(path:str = "HuggingFaceH4/no_robots", cache_dir:str = "./cache"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset['train_sft']
    recon_dataset = []
    for src in sources:
        output = src['messages'][1]['content']
        ins = src['messages'][0]['content']

        d = {"instruction": PT.format(ins), "output": output}
        recon_dataset.append(d)
    return recon_dataset


def UltraFeedback(path:str = "HuggingFaceH4/ultrafeedback_binarized", cache_dir:str = "./cache"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset['train_sft']
    recon_dataset = []
    for src in sources:
        output = src['chosen'][1]['content']
        ins = src['chosen'][0]['content']

        d = {"instruction": PT.format(ins), "output": output}
        recon_dataset.append(d)
    return recon_dataset


def OIGsmall(path:str = "heegyu/OIG-small-chip2-ko", cache_dir:str = "./cache"):
    dataset = datasets.load_dataset(path, cache_dir=cache_dir)
    sources = dataset['train']
    recon_dataset = []
    for src in sources:
        output = src['chip2_translated']
        ins = src['user_translated']
        d = {"instruction": PT.format(ins), "output": output}
        recon_dataset.append(d)
    return recon_dataset