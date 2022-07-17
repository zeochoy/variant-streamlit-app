import streamlit as st
import pandas as pd

# set up the variables
#DATA_PATH='data/demo-table_clean.tsv'
#MAIN_COLS=['Chr', 'Start', 'End', 'Ref', 'Alt', 'Mutation Type', 'Variant Type', 'Gene', 'Protein Change', 'Allele Freq', 'Functional Impact', 'Ref Reads', 'Variant Reads', 'Ref Reads (Normal)', 'Variant Reads (Normal)']

# set up the page config
st.set_page_config(page_title='Variants Viewer Demo', layout='wide')

# headings
st.title('Variants Viewer Demo')

st.header('Components')
st.write('1. Table Viewer')
st.write('2. Simple Statistics')

st.header('To-Do List')
to_dos = ['ACGS 2020 upgrade downgrade', 'Download notes & variant summary', 'CanVIG', 'Reminder of gene specific guideline']
for item in to_dos:
    st.checkbox(item, value=False)
