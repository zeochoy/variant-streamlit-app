import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from utils.utils import read_and_clean_data

### declare variables
DATA_PATH='data/demo-table_clean.tsv'
SELECTED_SUMMARY_COLS=['Variant Type', 'Mutation Type']
SELECTED_DIST_COLS=['VAF']

### read demo tsv
df = read_and_clean_data(DATA_PATH)

### header
st.header('Simple Statisitc')

### body
for c in SELECTED_SUMMARY_COLS:
    st.subheader(c)
    tmp_labels = df[c].unique()
    tmp_values = [len(df[df[c]==l]) for l in tmp_labels]
    fig = go.Figure(data=[go.Pie(labels=tmp_labels, values=tmp_values, hole=.3)])
    st.plotly_chart(fig, use_container_width=False)

for c in SELECTED_DIST_COLS:
    st.subheader(c)
    fig = ff.create_distplot([df[c].values], [c])
    st.plotly_chart(fig, use_container_width=False)
