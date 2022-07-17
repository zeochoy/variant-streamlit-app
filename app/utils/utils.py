import numpy as np
import pandas as pd
import streamlit as st

@st.cache(suppress_st_warning=True)
def read_and_clean_data(path):
    """
    read TSV table as pandas dataframe

    params:
        path (str): path of the annotated TSV

    return:
        sorted_df (pd.DataFrame)
    """
    tdf = pd.read_csv(path, sep='\t')
    tdf = tdf.assign(Depth=[f'{v}/{v+r}' for v,r in zip(tdf['Variant Depth'].values, tdf['Ref Depth'].values)])
    sorted_df = tdf.sort_values(by=['oncokb_level', 'cancer_hotspot', 'SIFT', 'PolyPhen2']).reset_index(drop=True)
    sorted_df = sorted_df.assign(ID=sorted_df.index.values)
    return sorted_df

@st.cache(suppress_st_warning=True)
def read_evidence_details(path):
    return pd.read_csv(path, sep='\t', index_col=0, header=None, squeeze=True)

def show_selected_row_details(row, cols_to_show):
    """
    show single/1st selected row from AgGrid

    params:
        row (pd.Series): single/1st selected row from AgGrid or any dictionary
        cols_to_show (list): list of fields to show

    return:
        print html table
    """
    #st.write(dict)
    row['dbSNP'] = dbsnp2html(row['dbSNP'])
    row['pop_freq'] = row['gnomAD']
    row['gnomAD'] = gnomad2html(row)
    row = row[cols_to_show]
    tdf = pd.DataFrame(row)
    style = tdf.style.hide(axis='columns')
    st.write(style.to_html(), unsafe_allow_html=True)
    return

def dbsnp2html(rsid):
    """
    generate html hyperlink to dbSNP from rsid

    params:
        rsid (str): RefSeq ID in dbSNP

    return:
        str: html hyperlink
    """
    if rsid!=np.nan:
        return f'<a target="_blank" href="https://www.ncbi.nlm.nih.gov/snp/{rsid}">{rsid}</a>'
    else:
        return

def gnomad2html(row):
    """
    generate html hyperlink to gnomAD from chr, start, end

    params:
        selected row (pd.Series): selected row from AgGrid

    return:
        str: html hyperlink
    """
    chr = row['Chr']
    start = row['Start']
    end = row['End']
    return f'<a target="_blank" href="https://gnomad.broadinstitute.org/region/{chr}-{start}-{end}?dataset=gnomad_r2_1">{chr}-{start}</a>'

def generate_acmg_evidence_table(path, evidence_details):
    """
    generate acmg evidence table
    """
    tdf = pd.read_csv(path, sep='\t', index_col=0)
    tdf = tdf.fillna('blank')
    evidence = list(set(tdf.to_numpy().flatten().tolist()))
    evidence.remove('blank')
    checked_evidence = []

    ### write header row
    #st.subheader('Evidence')
    headers = ['', '<h5 style="color:darkred;">Pathogenicity</h5>', '<h5 style="color:midnightblue;">Benign</h5>']
    hcols = st.columns([1,4,2])
    for i,h in enumerate(headers):
        hcols[i].write(f'{h}', unsafe_allow_html=True)
    scols = st.columns([1,1,1,1,1,1,1])
    columns = ['', 'Very Strong', 'Strong', 'Moderate','Supporting', 'Supporting', 'Strong']
    for i,c in enumerate(columns):
        scols[i].write(f'{c}')
    #st.markdown("""---""")
    ### write evidence row as checkbox
    for index, row in tdf.iterrows():
        scols = st.columns([1,1,1,1,1,1,1])
        #st.write(row)
        scols[0].write(f'{index}', unsafe_allow_html=True)
        for i,v in enumerate(row.values):
            if v != 'blank':
                tmp_val = v.split(', ')
                with scols[i+1]:
                    for tv in tmp_val:
                        tcb = st.checkbox(tv)
                        if tcb:
                            checked_evidence = update_list_of_evidence(tv, checked_evidence)

    ### write evidence details & classification
    if len(checked_evidence) > 0:
        #st.write(checked_evidence)
        st.write("")
        cols = st.columns([4,4])
        with cols[0]:
            with st.expander(f'{checked_evidence[-1]}', expanded=True):
                st.write(evidence_details[checked_evidence[-1]])
                st.text_area('Notes', placeholder=evidence_details[checked_evidence[-1]], height=5)
        with cols[1]:
            with st.expander('Classification', expanded=True):
                st.write(combine_evidence(checked_evidence), unsafe_allow_html=True)
                st.text_area('Summary', placeholder='Short summary about the variant', height=5)
    return


def update_list_of_evidence(criteria, checked_evidence):
    """
    update the list of seleted evidence

    params:
        criteria (str)
        checked_evidence (list)

    return:
        checked_evidence (list)
        """
    checked_evidence.append(criteria)
    return checked_evidence


def combine_evidence(checked_evidence):
    """
    combine evidence and compute the classification

    parmas:
        checked_evidence (list): list of selected evidence (string)

    returns:
        classifiation (str): HTML code on the classification
    """
    def get_evidence_level(criteria):
        if criteria != 'PVS1':
            lev = criteria[:2]
        else:
            lev = 'PVS'
        return lev

    ### count the evidence
    evidence_level = []
    for e in checked_evidence:
        evidence_level.append(get_evidence_level(e))
    n_pvs = evidence_level.count('PVS')
    n_ps = evidence_level.count('PS')
    n_pm = evidence_level.count('PM')
    n_pp = evidence_level.count('PP')
    n_ba = evidence_level.count('BA')
    n_bs = evidence_level.count('BS')
    n_bp = evidence_level.count('BP')

    #st.write(evidence_level)

    ### combine the evidence
    p_html = '<h3><span style="background-color:darkred; color:white;">Pathogenic</span></h3>'
    lp_html = '<h3><span style="background-color:tomato; color:white;">Likely Pathogenic</span></h3>'
    vus_html = '<h3><span style="background-color:darkgrey; color:white;">VUS</span></h3>'
    lb_html = '<h3><span style="background-color:lightskyblue; color:white;">Likely Benign</span></h3>'
    b_html = '<h3><span style="background-color:navy; color:white;">Benign</span></h3>'
    classification = vus_html
    if n_pvs > 0:
        if (n_ps > 0) or (n_pm > 1) or (n_pp>1) or (n_pm > 0 and n_pp > 0):
            classification = p_html
        elif (n_pm > 0):
            classification = lp_html
    elif n_ps > 0:
        if (n_ps > 1) or (n_pm > 2) or (n_pm > 1 and n_pp > 1) or (n_pm > 0 and n_pp > 3):
            classification = p_html
        elif (n_pm > 0) or (n_pp > 1):
            classification = lp_html
    elif n_pm > 2:
        classification = lp_html
    elif (n_pm > 1 and n_pp > 1):
        classification = lp_html
    elif (n_pm > 0 and n_pp >3):
        classification = lp_html
    elif n_ba > 0:
        classification = b_html
    elif n_bs > 1:
        classification = b_html
    elif (n_bs > 0 and n_bp > 0):
        classification = lb_html
    elif n_bp > 1:
        classification = lb_html
    else:
        classification = vus_html
    return classification


### Share google sheet via streamlit share -- advanced settings
# put this in the script
# gsheet_url = st.secrets["public_gsheets_url"]
# put this in the advanced settings
# gsheet_url = "the_link"
