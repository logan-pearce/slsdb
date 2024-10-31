import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc

from streamlit import session_state


st.title('Sirius-Like Systems Database')

st.markdown(
    """
    SLSdb is an interactive database of all known Sirius-Like Systems -- white dwarfs with non-interacting main sequence star companions of spectral type earlier than M. The Contents page walks through how we adapted multiple catalogs into the db.

    You can save the whole db using the download button on the upper right, or interact with the db using SQL interface to select desired columns/rows and save the subset. The plots below are interactive bokeh plots and can be zoomed, panned, and saved using the buttons in the upper right of the plot. If you select a subset of the data the plots will update automatically.
"""
)

#@st.cache_data
#### Render the db:
#slsdb = pd.read_csv('slsdb.csv')
#st.dataframe(slsdb)

### SQL interface:
conn = st.connection('slsdb', type='sql', url='postgresql:///github.com/logan-pearce/slsdb/blob/main/slsdb.db')

# if "query" not in st.session_state:
#     st.session_state.query = set()

def querySQL(string):
    session_state['db'] = conn.query(string)
    st.dataframe(session_state['db'])

# def querySQL(string):
#     q = conn.query(string)
#     return q


# with st.form(key="slsdbsql"):
#     st.text_input('SQL Query String', key='sqlquerystring')
#     st.form_submit_button('Query', on_click=querySQL(session_state['sqlquerystring']))
st.text_input('SQL Query String', key='sqlquerystring')

session_state['db'] = slsdb

#session_state
if session_state['sqlquerystring'] == '':
    session_state['db'] = slsdb
    st.dataframe(session_state['db'])
else:
    with st.form(key="slsdbsql"):
        st.form_submit_button('Query', on_click=querySQL(session_state['sqlquerystring']))



############# Visualize data:
st.title('Data Viz')

'''## Scatter Plot'''

plotcols = ("plx", "plx_err", "ra_j2000", "ra_j2000_err", "dec_j2000", "dec_j2000_err", "wd_vmag", "wd_gaia_g", "ms_vmag", "ms_gaia_g", "n_sys_components", "wd_ms_sep_au", "wd_ms_sep_as", "wd_ms_pa", "wd_spt", "wd_teff", "wd_logg", "wd_mass", "wd_mass_err", "wd_radius", "wd_cooling_age", "wd_cooling_age_plus", "wd_cooling_age_minus", "ms_spt", "ms_teff", "ms_logg", "ms_mass", "ms_radius", "ms_age", "ms_age_plus", "ms_age_minus", "sma", "sma_err_plus", "sma_err_minus", "per", "per_err_plus", "per_err_minus", "ecc", "ecc_err_plus", "ecc_err_minus", "inc", "inc_err_plus", "inc_err_minus", "argp", "argp_err_plus", "argp_err_minus", "lon", "lon_err_plus", "lon_err_minus", "t0", "t0_err_plus", "t0_err_minus")

col1, col2 = st.columns(2)
with col1:
    plotx = st.selectbox(
        "X axis",
        plotcols, key="plotx"
    )
with col2:
    ploty = st.selectbox(
        "Y axis",
        plotcols, key="ploty"
    )


col1, col2 = st.columns(2)
with col1:
    x_axis_type = st.radio("X axis", ['linear','log'], key='x_axis_type')
with col2:
    y_axis_type = st.radio("Y axis", ['linear','log'], key='y_axis_type')


chart_data = pd.DataFrame()
chart_data['x'] = session_state['db'][plotx]
chart_data['y'] = session_state['db'][ploty]
chart_data['color'] = session_state['db']['wd_mass']
chart_data['size'] = session_state['db']['ms_mass']
xlabel = plotx
ylabel = ploty

p = figure(x_axis_label=xlabel, y_axis_label=ylabel,
        background_fill_color='#222831', border_fill_color='#31363F',outline_line_color='#31363F',
        y_axis_type = session_state['y_axis_type'], x_axis_type = session_state['x_axis_type'])
p.yaxis.major_label_text_color = "#EEEEEE"
p.yaxis.axis_label_text_color = "#EEEEEE"
p.xaxis.major_label_text_color = "#EEEEEE"
p.xaxis.axis_label_text_color = "#EEEEEE"
p.grid.grid_line_color = '#EEEEEE'

p.circle(chart_data['x'], chart_data['y'], size=20, color="#76ABAE", alpha=0.7)
st.bokeh_chart(p, use_container_width=True)


'''## Histogram'''

plothist = st.selectbox(
        "Hist data",
        plotcols, key='plothist'
    )
bins = st.select_slider('Bins',key='bins',options=[10,25,50,100,500,1000])
x_axis_type_hist = st.radio("X axis", ['linear','log'], key='x_axis_type_hist')

xlabel = plothist
data = np.array(session_state['db'][plothist])
data = data[~np.isnan(data)]
phist = figure(x_axis_label=plothist,
        background_fill_color='#222831', border_fill_color='#31363F',outline_line_color='#31363F',
        x_axis_type = session_state['x_axis_type_hist'])

hist, edges = np.histogram(data, density=False, bins=bins)
phist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
         fill_color="#76ABAE", line_color="#EEEEEE")
phist.yaxis.major_label_text_color = "#EEEEEE"
phist.yaxis.axis_label_text_color = "#EEEEEE"
phist.xaxis.major_label_text_color = "#EEEEEE"
phist.xaxis.axis_label_text_color = "#EEEEEE"
phist.grid.grid_line_color = '#EEEEEE'
st.bokeh_chart(phist, use_container_width=True)