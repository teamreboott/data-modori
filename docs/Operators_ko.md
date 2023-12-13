# Operator 스키마

오퍼레이터(Operators)는 데이터 수정, 정리, 필터링, 중복 제거 등에서 도움이 되는 기본적인 프로세스 모음입니다. 우리는 다양한 데이터 소스와 파일 형식을 지원하며, 사용자 정의 데이터셋으로 유연하게 확장할 수 있습니다.

## 개요

Data-Juicer의 오퍼레이터는 5가지 유형으로 분류됩니다.

| 타입                                | 개수	 | 설명                                 |
|-----------------------------------|:------:|------------------------------------|
| [ Formatter ]( #formatter )       |   7    | 소스 데이터를 찾아서 로드하고 표준화합니다.        |
| [ Mapper ]( #mapper )             |   21   | 샘플을 편집하고 변환합니다.                    |
| [ Filter ]( #filter )             |   20   | 낮은 품질의 샘플을 필터링합니다.                 |
| [ Deduplicator ]( #deduplicator ) |   4    | 중복된 샘플을 감지하고 제거합니다.                |
| [ Selector ]( #selector )         |   2    | 랭킹 기준에 따라 상위 샘플을 선택합니다.            |


모든 구체적인 오퍼레이터는 아래에 나열되어 있으며, 각각이 여러 기능 태그로 표시됩니다.

* Domain Tags
  - General: 일반 목적
  - LaTeX: LaTeX 소스 파일에 특화됨
  - Code: 프로그래밍 코드에 특화됨
  - Financial: 금융 분야와 관련이 깊음
  - Image: 이미지 또는 멀티모달에 특화됨
  - Multimodal: 멀티모달에 특화됨
* Language Tags
    - en: English
    - ko: Korean


## Formatter <a name="formatter"/>

| Operator          | Domain  | Lang   | Description                                                                                     |
|-------------------|---------|--------|-------------------------------------------------------------------------------------------------|
| remote_formatter  | General | en, ko | 원격에서 데이터셋을 가져와 준비합니다 (예: HuggingFace)                                                           |
| csv_formatter     | General | en, ko | 로컬 `.csv` 파일을 준비합니다                                                                              |
| tsv_formatter     | General | en, ko | 로컬 `.tsv` 파일을 준비합니다                                                                              |
| json_formatter    | General | en, ko | 로컬 `.json`, `.jsonl`, `.jsonl.zst` 파일을 준비합니다                                                         |
| parquet_formatter | General | en, ko | 로컬 `.parquet` 파일을 준비합니다                                                                          |
| text_formatter    | General | en, ko | 기타 로컬 텍스트 파일을 준비합니다 ([complete list](../data_juicer/format/text_formatter.py#L63,73)) |
| mixture_formatter | General | en, ko | 모든 지원되는 로컬 파일 유형의 혼합을 처리합니다                                          | 


## Mapper <a name="mapper"/>

| Operator                                            | Domain             | Lang   | Description                                                                                                    |
|-----------------------------------------------------|--------------------|--------|----------------------------------------------------------------------------------------------------------------|
| clean_copyright_mapper                              | Code               | en, ko | Removes copyright notice at the beginning of code files (:warning: must contain the word *copyright*)          |
| clean_email_mapper                                  | General            | en, ko | Removes email information                                                                                      |
| clean_html_mapper                                   | General            | en, ko | Removes HTML tags and returns plain text of all the nodes                                                      |
| clean_ip_mapper                                     | General            | en, ko | Removes IP addresses                                                                                           |
| clean_links_mapper                                  | General, Code      | en, ko | Removes links, such as those starting with http or ftp                                                         |
| expand_macro_mapper                                 | LaTeX              | en, ko | Expands macros usually defined at the top of TeX documents                                                     |
| fix_unicode_mapper                                  | General            | en, ko | Fixes broken Unicodes (by [ftfy](https://ftfy.readthedocs.io/))                                                |
| nlpaug_en_mapper                                    | General            | en     | Simply augment texts in English based on the `nlpaug` library                                                  | 
| punctuation_normalization_mapper                    | General            | en, ko | Normalizes various Unicode punctuations to their ASCII equivalents                                             |
| remove_bibliography_mapper                          | LaTeX              | en, ko | Removes the bibliography of TeX documents                                                                      |
| remove_comments_mapper                              | LaTeX              | en, ko | Removes the comments of TeX documents                                                                          |
| remove_header_mapper                                | LaTeX              | en, ko | Removes the running headers of TeX documents, e.g., titles, chapter or section numbers/names                   |
| remove_long_words_mapper                            | General            | en, ko | Removes words with length outside the specified range                                                          |
| remove_non_chinese_character_mapper                 | General            | en, ko | Remove non Chinese character in text samples. |
| remove_specific_chars_mapper                        | General            | en, ko | Removes any user-specified characters or substrings                                                            |
| remove_table_text_mapper                            | General, Financial | en     | Detects and removes possible table contents (:warning: relies on regular expression matching and thus fragile) |
| remove_words_with_incorrect_<br />substrings_mapper | General            | en, ko | Removes words containing specified substrings                                                                  |
| sentence_split_mapper                               | General            | en     | Splits and reorganizes sentences according to semantics                                                        |
| whitespace_normalization_mapper                     | General            | en, ko | Normalizes various Unicode whitespaces to the normal ASCII space (U+0020)                                      |


## Filter <a name="filter"/>

| Operator                       | Domain  | Lang   | Description                                                                                |
|--------------------------------|---------|--------|--------------------------------------------------------------------------------------------|
| alphanumeric_filter            | General | en, ko | Keeps samples with alphanumeric ratio within the specified range                           |
| average_line_length_filter     | Code    | en, ko | Keeps samples with average line length within the specified range                          |
| character_repetition_filter    | General | en, ko | Keeps samples with char-level n-gram repetition ratio within the specified range           |
| clip_similarity_filter         | Multimodal |   -    |  Keeps samples with similarity between text and images within the specified range           |
| flagged_words_filter           | General | en, zh | Keeps samples with flagged-word ratio below the specified threshold                        |
| image_aspect_ratio_filter      | Image   |   -    | Keeps samples contains images with aspect ratios within specific range                     |
| image_shape_filter             | Image   |   -    | Keeps samples contains images with widths and heights within specific ranges               |
| image_size_filter              | Image   |   -    | Keeps samples contains images whose size in bytes are within specific range                     |
| language_id_score_filter       | General | en, ko | Keeps samples of the specified language, judged by a predicted confidence score            |
| maximum_line_length_filter     | Code    | en, ko | Keeps samples with maximum line length within the specified range                          |
| perplexity_filter              | General | en, ko | Keeps samples with perplexity score below the specified threshold                          |
| special_characters_filter      | General | en, ko | Keeps samples with special-char ratio within the specified range                           |
| specified_field_filter         | General | en, ko | Filters samples based on field, with value lies in the specified targets                   |
| specified_numeric_field_filter | General | en, ko | Filters samples based on field, with value lies in the specified range (for numeric types) |
| stopwords_filter               | General | en, ko | Keeps samples with stopword ratio above the specified threshold                            |
| suffix_filter                  | General | en, ko | Keeps samples with specified suffixes                                                      |
| text_length_filter             | General | en, ko | Keeps samples with total text length within the specified range                            |
| token_num_filter               | General | en, ko | Keeps samples with token count within the specified range                                  |
| word_num_filter                | General | en, ko | Keeps samples with word count within the specified range                                   |
| word_repetition_filter         | General | en, ko | Keeps samples with word-level n-gram repetition ratio within the specified range           |


## Deduplicator <a name="deduplicator"/>

| Operator                      | Domain  | Lang   | Description                                                 |
|-------------------------------|---------|--------|-------------------------------------------------------------|
| document_deduplicator         | General | en, ko | Deduplicate samples at document-level by comparing MD5 hash |
| document_minhash_deduplicator | General | en, ko | Deduplicate samples at document-level using MinHashLSH      |
| document_simhash_deduplicator | General | en, ko | Deduplicate samples at document-level using SimHash         |
| image_deduplicator            | Image   |   -    | Deduplicate samples at document-level using exact matching of images between documents |


## Selector <a name="selector"/>

| Operator                           | Domain  | Lang   | Description                                                           |
|------------------------------------|---------|--------|-----------------------------------------------------------------------|
| frequency_specified_field_selector | General | en, ko | Selects top samples by comparing the frequency of the specified field |
| topk_specified_field_selector      | General | en, ko | Selects top samples by comparing the values of the specified field    |


## Contributing
We welcome contributions of adding new operators. Please refer to [How-to Guide for Developers](DeveloperGuide_en.md).