# Operator Schemas

Operators are a collection of basic processes that assist in data modification, cleaning, filtering, deduplication, etc. We support a wide range of data sources and file formats, and allow for flexible extension to custom datasets.


## Overview

The operators in Data-Juicer are categorized into 5 types.

| Type                              | Number | Description                                     |
|-----------------------------------|:------:|-------------------------------------------------|
| [ Formatter ]( #formatter )       |   7    | Discovers, loads, and canonicalizes source data |
| [ Mapper ]( #mapper )             |   18   | Edits and transforms samples                    |
| [ Filter ]( #filter )             |   16   | Filters out low-quality samples                 |
| [ Deduplicator ]( #deduplicator ) |   3    | Detects and removes duplicate samples           |
| [ Selector ]( #selector )         |   2    | Selects top samples based on ranking            |


All the specific operators are listed below, each featured with several capability tags.

* Domain Tags
    - General: general purpose
    - LaTeX: specific to LaTeX source files
    - Code: specific to programming codes
    - Financial: closely related to financial sector
    - Image: specific to image or multimodal
    - Multimodal: specific to multimodal
* Language Tags
    - en: English
    - ko: Korean


## Formatter <a name="formatter"/>

| Operator          | Domain  | Lang   | Description                                                                                       |
|-------------------|---------|--------|---------------------------------------------------------------------------------------------------|
| remote_formatter  | General | en, ko | Prepares datasets from remote (e.g., HuggingFace)                                                 |
| csv_formatter     | General | en, ko | Prepares local `.csv` files                                                                       |
| tsv_formatter     | General | en, ko | Prepares local `.tsv` files                                                                       |
| json_formatter    | General | en, ko | Prepares local `.json`, `.jsonl`, `.jsonl.zst` files                                              |
| parquet_formatter | General | en, ko | Prepares local `.parquet` files                                                                   |
| text_formatter    | General | en, ko | Prepares other local text files ([complete list](../data_modori/format/text_formatter.py#L63,73)) |
| mixture_formatter | General | en, ko | Handles a mixture of all the supported local file types                                           | 


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
| flagged_words_filter           | General | en, ko | Keeps samples with flagged-word ratio below the specified threshold                        |
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


## Selector <a name="selector"/>

| Operator                           | Domain  | Lang   | Description                                                           |
|------------------------------------|---------|--------|-----------------------------------------------------------------------|
| frequency_specified_field_selector | General | en, ko | Selects top samples by comparing the frequency of the specified field |
| topk_specified_field_selector      | General | en, ko | Selects top samples by comparing the values of the specified field    |


## Contributing
We welcome contributions of adding new operators. Please refer to [How-to Guide for Developers](DeveloperGuide_en.md).
