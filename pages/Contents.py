import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
import sys

from streamlit import session_state

st.set_page_config(
        page_title="SLSdb",
        page_icon="",
        layout="wide",
    )

sidebar_logo = 'images/slsdb-logo-3.png'
st.logo(sidebar_logo, size='large')



cols = ['wd_name', 'ms_simbadable_name', 'disc_ref', 'disc_type', 'note',
       'resolved', 'resolved_ref', 'confirmed', 'confirmed_ref',
       'wd_gaia_sourceid', 'ms_gaia_sourceid', 'plx', 'plx_err', 'ra_j2000',
       'ra_j2000_err', 'dec_j2000', 'dec_j2000_err', 'plx_coord_source',
       'wd_vmag', 'wd_gaia_g', 'ms_vmag', 'ms_gaia_g', 'n_sys_components',
       'wd_ms_sep_au', 'wd_ms_sep_as', 'wd_ms_pa', 'sep_pa_date', 'sep_pa_ref',
       'wd_spt', 'wd_teff', 'wd_logg', 'wd_mass', 'wd_mass_err', 'dyn_mass',
       'wd_radius', 'wd_cooling_age', 'wd_cooling_age_plus',
       'wd_cooling_age_minus', 'wd_properties_refs', 'ms_spt', 'ms_teff',
       'ms_logg', 'ms_mass', 'ms_radius', 'ms_age', 'ms_age_plus',
       'ms_age_minus', 'ms_properties_refs', 'wd_known_polluted',
       'pollution_reference', 'has_orbit', 'sma', 'sma_err_plus',
       'sma_err_minus', 'per', 'per_err_plus', 'per_err_minus', 'ecc',
       'ecc_err_plus', 'ecc_err_minus', 'inc', 'inc_err_plus', 'inc_err_minus',
       'argp', 'argp_err_plus', 'argp_err_minus', 'lon', 'lon_err_plus',
       'lon_err_minus', 't0', 't0_err_plus', 't0_err_minus', 'error_format',
       'orbit_params_ref']
st.code(cols, language = "python")

query_h = '''
cat = 'J/MNRAS/435/2077'
from astroquery.vizier import Vizier
Vizier.ROW_LIMIT = -1
h = Vizier.get_catalogs(cat)
h = h[0].to_pandas()'''
st.code(query_h, language = "python")

strng = 's = pd.DataFrame(columns = names)'

