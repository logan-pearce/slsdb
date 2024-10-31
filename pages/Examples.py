import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc

from streamlit import session_state

st.set_page_config(
        page_title="SLSdb",
        page_icon="",
        layout="wide",
    )

'''## Querying the slsdb with SQL

SQL is a language for selecting specific elements from a database. After entering a query in the text box, the SLSdb app will display the results and everything on the main page will update to use only the results from the query. To return to the whole database, reload the page.
'''


'''## Example basic SQL queries'''

''' ### Select every column for a specific SLS '''
strg = "SELECT * FROM slsdb WHERE ms_simbadable_name = 'Sirius'"
st.code(strg, language="sql")
'''Note: strings must be enclosed in quotes, floats or integrers should not'''

''' ### Select specific columns'''
strg = "SELECT wd_gaia_sourceid, wd_gaia_g FROM slsdb WHERE ms_simbadable_name = 'Sirius'"
st.code(strg, language="sql")
'''Note: this will cause errors for the plots on the main page if you select only columns not displayed on the plot. This is fine.'''

''' ### Select the brightest hosts '''
strg = "SELECT * FROM slsdb WHERE ms_gaia_g < 5"
st.code(strg, language="sql")

''' ### Select SLS within a rectangular region'''
strg = "SELECT * FROM slsdb WHERE ra_j2000 BETWEEN 30 AND 40 AND dec_j2000 BETWEEN 45 and 60"
st.code(strg, language="sql")

''' ### How many SLS would be visible to Las Campanas Observatory during a specific RA range? '''
strg = "SELECT count(*) FROM slsdb WHERE ra_j2000 BETWEEN 0 AND 65 AND dec_j2000 BETWEEN -60 and 20"
st.code(strg, language="sql")