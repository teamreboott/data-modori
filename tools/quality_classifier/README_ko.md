# Quality Classifier Toolkit

Quality Classifier Toolkit는 GPT-3 품질 분류기와 유사한 방식으로 웹 데이터셋에 대한 품질 분류를 복제하고 적용하는 데 도움이 되는 도구 모음입니다.

이 전체 도구 모음은 PySpark를 기반으로 하며, 여기에서의 품질 분류기의 기본 구조는 다음과 같습니다:
- tokenizer: PySpark의 [standard Tokenizer](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.Tokenizer.html#tokenizer) 또는 [sentencepiece](https://github.com/google/sentencepiece 모델
- feature extractor: [HashingTF](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.HashingTF.html#hashingtf)
- classifier: [LogisticRegression](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.classification.LogisticRegression.html#logisticregression)

## 사용법

### 기존 분류기로 예측하기

`predict.py` 를 사용하여 "품질"에 대한 문서 점수를 예측하고 각 샘플에 대해 이 샘플이 해당 점수에 따라 유지되어야 하는지를 나타내는 레이블을 예측합니다.

```shell
# predict doc_score for a dataset
python predict.py \
    <dataset_path> \
    <result_path> \
    [--model <model_path>] \
    [--tokenizer <tokenizer_type>] \
    [--keep_method <keep_method>] \
    [--text_key <text_key>] \
    [--overall_stats]

# 사용법 메시지 출력
python predict.py --help
```

- `dataset_path`: 입력 데이터셋 경로입니다. 경로의 접미사는 `[json, jsonl, parquet]` 중 하나여야 합니다.
- `result_path`: 예측 결과를 저장할 데이터셋의 경로입니다. 경로의 접미사는 `[json, jsonl, parquet]` 중 하나여야 합니다.
- `model_path`: (선택 사항. 기본값: "gpt3") 예측에 사용할 모델의 경로입니다. 제공된 모델 중 하나를 사용할 수 있습니다 `[gpt3, chinese, code]`. 또는 `train.py` 스크립트를 사용하여 직접 훈련한 모델을 사용할 수 있습니다.
- `tokenizer`: (선택 사항. 기본값: None) 분류할 텍스트를 토큰화하기 위한 토크나이저입니다. None이면 PySpark의 [standard Tokenizer](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.Tokenizer.html#tokenizer)가 사용됩니다. 또한 제공된 토크나이저 중 하나를 사용할 수 있습니다 `[zh.sp.model, code.sp.model]`. 또는 자체 [sentencepiece](https://github.com/google/sentencepiece) 모델의 경로로 설정할 수 있습니다.
- `keep_method`: (선택 사항. 기본값: "gpt3") doc_score에 따라 샘플을 유지할지 여부를 결정하는 데 사용되는 방법입니다. `[gpt3, label]` 중 하나여야 합니다.
- `text_key`: (선택 사항. 기본값: "text") 입력 데이터셋에 있는 분류할 텍스트를 저장하는 필드 이름입니다.
- `overall_stats`: (선택 사항. 기본값: False) 문서 점수의 전체 통계 보고서를 생성할지 여부입니다.

### 자체 품질 분류기 훈련하기

`train.py`를 사용하여 자체 데이터셋에 대한 품질 분류기를 훈련합니다.

```shell
# 자체 데이터셋에 대한 품질 분류기 훈련
python train.py \
    <positive_datasets>] \
    <negative_datasets>] \
    [--output_model_path <model_name>] \
    [--num_training_samples <num_training_samples>] \
    [--train_test_split_ratio <train_test_split_ratio>] \
    [--tokenizer <tokenizer_type>] \
    [--evaluation <evaluation>] \
    [--text_key <text_key>]

# 사용법 메시지 출력
python train.py --help
```

- `positive_datasets`: 긍정적인 데이터셋의 경로입니다. 단일 데이터셋에 대한 문자열일 수 있습니다. 예: `'pos.parquet'`, 또는 여러 데이터셋에 대한 문자열 목록일 수 있습니다. 예: `'["pos1.parquet", "pos2.parquet"]'`.
- `negative_datasets`: 부정적인 데이터셋의 경로입니다. `positive_datasets`와 유사합니다.
- `output_model_path`: (Optional. Default: "my_quality_model") the path to store the trained classifier.
- `num_training_samples`: (Optional. Default: 0) number of samples used to train the model for pos/neg datasets respectively. Default 0 means using all samples to train.
- `train_test_split_ratio`: (Optional. Default: 0.8) ratio to split training set, and the rest of samples will be test set used to evaluate.
- `tokenizer`: (Optional. Default: None) the tokenizer to tokenize texts to be classified. If it's None, the [standard Tokenizer](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.Tokenizer.html#tokenizer) of PySpark will be used. Besides, you can use one of the tokenizers we provide `[zh.sp.model, code.sp.model]`. Or you can set it to a path to your own [sentencepiece](https://github.com/google/sentencepiece) model.
- `evaluation`: (Optional, Default: True) whether to evaluate the trained classifier using the test set after training.
- `text_key`: (Optional. Default: "text") the field name to store texts to be classified in the input dataset.

### Evaluate a quality classifier

Use `eval.py` to evaluate a quality classifier to report Precision, Recall, and F1 metrics.

```shell
# evaluate a quality classifier on your own dataset
python eval.py \
    [--positive_datasets <positive_datasets>] \
    [--negative_datasets <negative_datasets>] \
    [--model <model_path>] \
    [--tokenizer <tokenizer_type>] \
    [--text_key <text_key>]

# print the usage message
python eval.py --help
```

- `positive_datasets`: (Optional. Default: None) the paths to the positive datasets. It could be a string for a single dataset, e.g. `'pos.parquet'`, or a list of strings for multiple datasets, e.g. `'["pos1.parquet", "pos2.parquet"]'`.
- `negative_datasets`: (Optional. Default: None) the paths to the negative datasets. Similar to `positive_datasets`.
- `model_path`: (Optional. Default: "my_quality_model") the path to the model to be evaluated. You can evaluate one of the models we provide `[gpt3, chinese, code]`. Or you can evaluate the model trained by yourself using the `train.py` script.
- `tokenizer`: (Optional. Default: None) the tokenizer to tokenize texts to be classified. If it's None, the [standard Tokenizer](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.Tokenizer.html#tokenizer) of PySpark will be used. Besides, you can use one of the tokenizers we provide `[zh.sp.model, code.sp.model]`. Or you can set it to a path to your own [sentencepiece](https://github.com/google/sentencepiece) model.
- `text_key`: (Optional. Default: "text") the field name to store texts to be classified in the input dataset.

## Model Zoo

We provide 3 models we trained before: `gpt3`, `chinese`, `code`. Each model has its tokenizer and keep method. Tokenizers "xx.sp.model" are trained on the training data using [sentencepiece](https://github.com/google/sentencepiece).

| model     | tokenizer          | keep method      | positive datasets                                  | negative datasets                        |
|-----------|--------------------|------------------|----------------------------------------------------|------------------------------------------|
| `gpt3`    | standard Tokenizer | pareto           | Wikipedia-en & books1 & OpenWebText2               | CommonCrawl                              |
| `chinese` | zh.sp.model        | label            | Wikipedia-zh & Wudao                               | Samples in Chinese from CommonCrawl      |
| `code`    | code.sp.model      | label            | Samples with max_stars_count >= 1372 from TheStack | Random samples from the rest of TheStack |

- `gpt3`: GPT-3 quality classifier reproduced by us.
- `chinese`: A Chinese quality classifier trained by the same pipeline as `gpt3`, but with different tokenizer and training data.
- `code`: (Experimental) A code quality classifier trained by the same pipeline as `gpt3`, but with different tokenizer and training data. We only keep "programming" and "markup" language types of samples for training.
- Experiments of these classifiers on corresponding test sets are shown in the table below:

| model     | Precision  | Recall | F1     |
|-----------|------------|--------|--------|
| `gpt3`    | 96.82%     | 98.14% | 97.47% |
| `chinese` | 98.00%     | 99.30% | 98.64% |
| `code`    | 71.23%     | 54.21% | 61.56% |

- Keep ratios of `gpt3` and `chiense` classifiers on CommonCrawl are shown in the table below:

| model                                | keep ratio @ label  | keep ratio @ pareto |
|--------------------------------------|---------------------|---------------------|
| GPT-3 quality classifier (estimated) | -                   | ~1.3%               |
| `gpt3`                               | 3.22%               | 1.41%               |
| `chinese`                            | 1.81%               | -                   |

## More about Quality Classifier

### Method

The quality classifiers here mainly refer to the GPT-3 quality classifier mentioned in the Appendix A of GPT-3 paper:

> In order to improve the quality of Common Crawl, we developed an automatic filtering method to remove low quality documents. Using the original WebText as a proxy for high-quality documents, we trained a classifier to distinguish these from raw Common Crawl. We then used this classifier to re-sample Common Crawl by prioritizing documents which were predicted by the classifier to be higher quality. The classifier is trained using logistic regression classifier with features from Spark’s standard tokenizer and HashingTF 10. For the positive examples, we used a collection of curated datasets such as WebText, Wikiedia, and our web books corpus as the positive examples, and for the negative examples, we used unfiltered Common Crawl. We used this classifier to score Common Crawl documents. We kept each document in our dataset iff
>
>     np.random.pareto(α) > 1 − document_score
>
> We chose α = 9 in order to take mostly documents the classifier scored highly, but still include some documents that were out of distribution. α was chosen to match the distribution of scores from our classifier on WebText. We found this re-weighting increased quality as measured by loss on a range of out-of-distribution generative text samples.

### Tokenizers

- Standard Tokenizer in Spark: split texts by whitespaces.
- zh/code.sp.model: trained using sentencepiece.

### Keep Methods
- label: `doc_score > 0.5`
- pareto: `doc_score > 1 - np.random.pareto(α), α = 9`
