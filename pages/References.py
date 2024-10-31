import streamlit as st
import pandas as pd
import numpy as np

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

# sheetname = 43586033
# sheetid = '169q8SLAi6ujjjPr-x-hiTd4SA4ZVBSu3BubUYxqVHzg'
# refs = GetSheet(sheet_id = sheetid, sheet_name = sheetname)
# refs.to_csv('refs.csv', index=False)
refs = pd.read_csv('refs.csv')

st.dataframe(refs)