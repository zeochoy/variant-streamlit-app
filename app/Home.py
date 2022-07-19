import streamlit as st
import pandas as pd

# set up the page config
st.set_page_config(page_title='Variants Viewer Demo', layout='wide')

# headings
st.title('Variants Viewer Demo')
st.write('A variant viewer dashboard to browse annotated variant calling result.')
st.write('Intended for _DEMO_ only, not for production use.')
st.write("---")

st.header('Components')
st.write('1. Simple Statistics')
st.write('2. Table Viewer')
st.write("---")

st.header('To-Do List')
to_dos = ['ACGS 2020 upgrade downgrade', 'Download notes & variant summary', 'CanVIG', 'Reminder of gene specific guideline']
for item in to_dos:
    st.checkbox(item, value=False)
