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

sidebar_logo = 'images/slsdb-logo-3.png'
st.logo(sidebar_logo, size='large')