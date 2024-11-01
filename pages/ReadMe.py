import streamlit as st
import pandas as pd
import numpy as np

st.title('The Sirius-Like Systems Database')

st.markdown(
    """
    SLSdb is an interactive database of all known Sirius-Like Systems -- white dwarfs with non-interacting main sequence star companions of spectral type earlier than M. View the Tutorials page for how to interact with the db; the Derivation page walks through how we adapted multiple catalogs into the db.

### Contibuting
To contribute to slsdb please email Logan Pearce at lapearce@umich.edu

### Future Upgrades
 - Allow users to submit new SLS

"""
)

'''
## Columns
'''

# def GetSheet(sheet_id='1rD4aVpD57SQuPR8f2cqb2IJT67KlOg9NNnOu0lbUqGg', 
#              sheet_name=0):
#     url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={sheet_name}"
#     p = pd.read_csv(url)
#     p = p.dropna(axis=1, how='all')
#     for i in range(len(p)):
#         try:
#             if np.isnan(p[p.columns[0]][0]):
#                 p = p.drop(i, axis=0)
#         except TypeError:
#             pass
#     return p

# sheetname = 0
# sheetid = '169q8SLAi6ujjjPr-x-hiTd4SA4ZVBSu3BubUYxqVHzg'
# cols = GetSheet(sheet_id = sheetid, sheet_name = sheetname)
# cols.to_csv('Cols.csv', index=False)
st.set_page_config(
        page_title="SLSdb",
        page_icon="images/slsdb-logo-3.png",
        layout="wide",
    )

sidebar_logo = 'images/slsdb-logo-3.png'
st.logo(sidebar_logo, size='large')

cols = pd.read_csv('Cols.csv')
st.dataframe(cols)