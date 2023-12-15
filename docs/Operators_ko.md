# Operator 스키마

오퍼레이터(Operators)는 데이터 수정, 정리, 필터링, 중복 제거 등에서 도움이 되는 기본적인 프로세스 모음입니다. 우리는 다양한 데이터 소스와 파일 형식을 지원하며, 사용자 정의 데이터셋으로 유연하게 확장할 수 있습니다.

## 개요

Data-Juicer의 오퍼레이터는 5가지 유형으로 분류됩니다.

| 타입                                | 개수	 | 설명                                |
|-----------------------------------|:------:|------------------------------------|
| [ Formatter ]( #formatter )       |   7    | 소스 데이터를 찾아서 로드하고 표준화합니다.   |
| [ Mapper ]( #mapper )             |   18   | 샘플을 편집하고 변환합니다.               |
| [ Filter ]( #filter )             |   16   | 낮은 품질의 샘플을 필터링합니다.           |
| [ Deduplicator ]( #deduplicator ) |   3    | 중복된 샘플을 감지하고 제거합니다.          |
| [ Selector ]( #selector )         |   2    | 랭킹 기준에 따라 상위 샘플을 선택합니다.     |


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
| text_formatter    | General | en, ko | 기타 로컬 텍스트 파일을 준비합니다 ([complete list](../data_modori/format/text_formatter.py#L63,73)) |
| mixture_formatter | General | en, ko | 모든 지원되는 로컬 파일 유형의 혼합을 처리합니다                                          | 


## Mapper <a name="mapper"/>

| Operator                                            | Domain             | Lang   | Description                                                                                      |
|-----------------------------------------------------|--------------------|--------|--------------------------------------------------------------------------------------------------|
| clean_copyright_mapper                              | Code               | en, ko | 코드 파일의 시작 부분에 있는 저작권 표시를 제거합니다 (:warning: must contain the word *copyright*)  |
| clean_email_mapper                                  | General            | en, ko | 이메일 정보를 제거합니다                                                                          |
| clean_html_mapper                                   | General            | en, ko | HTML 태그를 제거하고 모든 노드의 일반 텍스트를 반환합니다                                            |
| clean_ip_mapper                                     | General            | en, ko | IP 주소를 제거합니다                                                                              |
| clean_links_mapper                                  | General, Code      | en, ko | 링크를 제거합니다 (예: http 또는 ftp로 시작하는 링크)                                            |
| expand_macro_mapper                                 | LaTeX              | en, ko | TeX 문서 상단에 일반적으로 정의된 매크로를 확장합니다                                            |
| fix_unicode_mapper                                  | General            | en, ko | 깨진 유니코드를 수정합니다 (by [ftfy](https://ftfy.readthedocs.io/))                                  |
| nlpaug_en_mapper                                    | General            | en     | `nlpaug` 라이브러리를 기반으로 영어 텍스트를 단순히 증가시킵니다                                       | 
| punctuation_normalization_mapper                    | General            | en, ko | 다양한 유니코드 구두점을 해당 ASCII 등가물로 표준화합니다                                     |
| remove_bibliography_mapper                          | LaTeX              | en, ko | TeX 문서의 참고문헌을 제거합니다                                                           |
| remove_comments_mapper                              | LaTeX              | en, ko | TeX 문서의 주석을 제거합니다                                                              |
| remove_header_mapper                                | LaTeX              | en, ko | TeX 문서의 러닝 헤더를 제거합니다, e.g., titles, chapter or section numbers/names      |
| remove_long_words_mapper                            | General            | en, ko | 지정된 범위를 벗어나는 길이의 단어를 제거합니다                                               |
| remove_specific_chars_mapper                        | General            | en, ko | 사용자가 지정한 문자나 부분 문자열을 제거합니다                                                |
| remove_table_text_mapper                            | General, Financial | en     | 가능한 테이블 콘텐츠를 감지하고 제거합니다 (:warning: relies on regular expression matching and thus fragile) |
| remove_words_with_incorrect_<br />substrings_mapper | General            | en, ko | 지정된 부분 문자열을 포함하는 단어를 제거합니다                                                     |
| sentence_split_mapper                               | General            | en     | 문장을 의미에 따라 분리하고 재구성합니다                                            |
| whitespace_normalization_mapper                     | General            | en, ko | 다양한 유니코드 공백을 정규 ASCII 공백 (U+0020)으로 정규화합니다                         |


## Filter <a name="filter"/>

| Operator                       | Domain  | Lang   | Description                                                                        |
|--------------------------------|---------|--------|------------------------------------------------------------------------------------|
| alphanumeric_filter            | General | en, ko | 알파벳 및 숫자 비율이 지정된 범위 내에 있는 샘플을 유지합니다.                                               |
| average_line_length_filter     | Code    | en, ko | 평균 줄 길이가 지정된 범위 내에 있는 샘플을 유지합니다.                                                   |
| character_repetition_filter    | General | en, ko | 문자 수준 n-그램 반복 비율이 지정된 범위 내에 있는 샘플을 유지합니다.                                          |
| flagged_words_filter           | General | en, ko | flagged-word 비율이 지정된 임계값 아래인 샘플을 유지합니다.                                            |
| language_id_score_filter       | General | en, ko | 예측된 신뢰도 점수에 따라 특정 언어의 샘플을 유지합니다.                                                   |
| maximum_line_length_filter     | Code    | en, ko | 최대 줄 길이가 지정된 범위 내에 있는 샘플을 유지합니다.                                                   |
| perplexity_filter              | General | en, ko | perplexity 점수가 지정된 임계값 아래인 샘플을 유지합니다.                                              |
| special_characters_filter      | General | en, ko | 특수 문자 비율이 지정된 범위 내에 있는 샘플을 유지합니다.                        |
| specified_field_filter         | General | en, ko | 필드를 기반으로 샘플을 필터링하고, 값이 지정된 대상 내에 있는 경우 유지합니다.
| specified_numeric_field_filter | General | en, ko | 필드를 기반으로 샘플을 필터링하고, 값이 지정된 범위 내에 있는 경우 유지합니다. (숫자 유형에 대한 경우) |
| stopwords_filter               | General | en, ko | 불용어 비율이 지정된 임계값 위인 샘플을 유지합니다.                         |
| suffix_filter                  | General | en, ko | 지정된 접미사를 갖는 샘플을 유지합니다.                                               |
| text_length_filter             | General | en, ko | 지정된 범위 내의 전체 텍스트 길이를 갖는 샘플을 유지합니다.                       |
| token_num_filter               | General | en, ko | 지정된 범위 내의 토큰 수를 갖는 샘플을 유지합니다.                            |
| word_num_filter                | General | en, ko | 지정된 범위 내의 단어 수를 갖는 샘플을 유지합니다.                            |
| word_repetition_filter         | General | en, ko | 지정된 범위 내의 단어 수준 n-그램 반복 비율을 갖는 샘플을 유지합니다.    |


## Deduplicator <a name="deduplicator"/>

| Operator                      | Domain  | Lang   | Description                                             |
|-------------------------------|---------|--------|---------------------------------------------------------|
| document_deduplicator         | General | en, ko | MD5 해시를 비교하여 문서 수준에서 샘플 중복 제거 |
| document_minhash_deduplicator | General | en, ko | MinHashLSH를 사용하여 문서 수준에서 샘플 중복 제거    |
| document_simhash_deduplicator | General | en, ko | SimHash를 사용하여 문서 수준에서 샘플 중복 제거       |


## Selector <a name="selector"/>

| Operator                           | Domain  | Lang   | Description                                                         |
|------------------------------------|---------|--------|---------------------------------------------------------------------|
| frequency_specified_field_selector | General | en, ko | 지정된 필드의 빈도를 비교하여 상위 샘플을 선택합니다. |
| topk_specified_field_selector      | General | en, ko | 지정된 필드의 값 비교를 통해 상위 샘플을 선택합니다.   |


## Contributing
새로운 연산자를 추가하는 기여를 환영합니다. [개발자를 위한 How-to 가이드](DeveloperGuide_ko.md)를 참조하세요.
