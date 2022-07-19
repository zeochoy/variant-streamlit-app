import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from utils.utils import read_and_clean_data, show_selected_row_details, generate_acmg_evidence_table, read_evidence_details

### declare variables
DATA_PATH='data/demo-table_clean.tsv'
ACMG_TABLE_PATH='data/acmg_evidence_table.tsv'
ACMG_DETAILS_PATH='data/acmg_evidence_details.tsv'
#ACMG_PATHO_TABLE_PATH='data/acmg_criteria_table_pathogenic.tsv'
#ACMG_BENIGN_TABLE_PATH='data/acmg_criteria_table_benign.tsv'
MAIN_COLS=['Gene', 'Protein Change', 'HGVSg', 'VAF', 'Depth', 'oncokb_level', 'ClinVar_ClinSig', 'cancer_hotspot', 'SIFT', 'PolyPhen2']
DETAIL_COLS=['Gene', 'HGVSg', 'HGVSc', 'Exon', 'pop_freq', 'gnomAD', 'ClinVar_ClinSig', 'dbSNP']

### read demo tsv
df = read_and_clean_data(DATA_PATH)

### header
st.header('Variant Table')

### body
### set up aggrid
gb = GridOptionsBuilder.from_dataframe(df[MAIN_COLS])
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_selection(selection_mode='single', use_checkbox=True)
gridOptions = gb.build()

update_data = AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.SELECTION_CHANGED)

### show details of selected row
selected_rows = update_data['selected_rows']
if len(selected_rows) != 0:
    show_selected_row_details(pd.Series(selected_rows[0]), DETAIL_COLS)

### test
st.write("---")
acmg_details = read_evidence_details(ACMG_DETAILS_PATH)
generate_acmg_evidence_table(ACMG_TABLE_PATH, acmg_details)
