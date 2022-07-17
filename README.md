# Variant Viewer (streamlit)
A variant viewer dashboard to browse annotated variant calling result.
**Intended for _DEMO_ only, not for production use.**

## Demo
https://share.streamlit.io/zeochoy/variant-streamlit-app/app/Home.py

## Usage
```
streamlit run app/Home.py
```

## Dependencies
streamlit aggrid numpy scipy pandas plotly

## Directory
```
.
|-- README.md
|-- app
|   |-- Home.py
|   |-- pages
|   |   |-- 1_Variant_Table_Viewer.py
|   |   `-- 2_Simple_Statistics.py
|   `-- utils
|       `-- utils.py
|-- data
|   |-- acmg_evidence_details.tsv
|   |-- acmg_evidence_table.tsv
|   |-- demo-table.tsv
|   `-- demo-table_clean.tsv
`-- requirements.txt
```
