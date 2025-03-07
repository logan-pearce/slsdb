import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.palettes import Magma256, Viridis256

from streamlit import session_state

st.set_page_config(
        page_title="SLSdb",
        page_icon="images/slsdb-logo-3.png",
        layout="wide",
    )

sidebar_logo = 'images/slsdb-logo-3.png'
st.logo(sidebar_logo, size='large')

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('images/slsdb-logo.png', width=300)
st.title('Sirius-Like Systems Database')

st.markdown(
    """
    SLSdb is an interactive database of all known Sirius-Like Systems -- white dwarfs with non-interacting main sequence star companions of spectral type earlier than M. The Contents page walks through how we adapted multiple catalogs into the db.

    You can save the whole db using the download button on the upper right, or interact with the db using SQL interface to select desired columns/rows and save the subset. The plots below are interactive bokeh plots and can be zoomed, panned, and saved using the buttons in the upper right of the plot. If you select a subset of the data the plots will update automatically.
"""
)

#@st.cache_data
#### Render the db:
slsdb = pd.read_csv('slsdb.csv')

plotcols = ("plx", "plx_err", "ra_j2000", "ra_j2000_err", "dec_j2000", "dec_j2000_err", "wd_vmag", "wd_gaia_g", "ms_vmag", "ms_gaia_g", "n_sys_components", "wd_ms_sep_au", "wd_ms_sep_as", "wd_ms_pa", "wd_spt", "wd_teff", "wd_logg", "wd_mass", "wd_mass_err", "wd_radius", "wd_cooling_age", "wd_cooling_age_plus", "wd_cooling_age_minus", "ms_spt", "ms_teff", "ms_logg", "ms_mass", "ms_radius", "ms_age", "ms_age_plus", "ms_age_minus", "sma", "sma_err_plus", "sma_err_minus", "per", "per_err_plus", "per_err_minus", "ecc", "ecc_err_plus", "ecc_err_minus", "inc", "inc_err_plus", "inc_err_minus", "argp", "argp_err_plus", "argp_err_minus", "lon", "lon_err_plus", "lon_err_minus", "t0", "t0_err_plus", "t0_err_minus")
for col in plotcols:
    slsdb.loc[np.where(slsdb[col] == '--')[0],col] = np.nan

slsdb.loc[np.where(slsdb['ra_j2000'] == '--')[0],'ra_j2000'] = np.nan
slsdb.loc[np.where(slsdb['dec_j2000'] == '--')[0],'dec_j2000'] = np.nan
slsdb.loc[np.where(slsdb['plx'] == '--')[0],'plx'] = np.nan
slsdb.loc[np.where(slsdb['ms_gaia_g'] == '--')[0],'ms_gaia_g'] = np.nan


import sqlite3
conn = sqlite3.connect('slsdb.db')
slsdb.to_sql('slsdb.db',conn,index=False, if_exists='append')


### SQL interface:
conn = st.connection('slsdb', type='sql', url = "sqlite:///slsdb.db")


def querySQL(string):
    session_state['db'] = conn.query(string)
    st.dataframe(session_state['db'])

st.text_input(r"$\textsf{\Large SQL Query String}$", key='sqlquerystring')

session_state['db'] = slsdb

#session_state
if session_state['sqlquerystring'] == '':
    session_state['db'] = slsdb
    st.dataframe(session_state['db'])
else:
    with st.form(key="slsdbsql"):
        st.form_submit_button('Query', on_click=querySQL(session_state['sqlquerystring']))



### RA/DEC Plot::::
from bokeh.models import LinearColorMapper, ColumnDataSource, LinearInterpolator, ColorBar, Label
from bokeh.transform import linear_cmap, log_cmap

multiplier = 100
st.text('Marker size corresponds to MS g magnitude; marker color corresponds to distance')

datadf = pd.DataFrame(data={'plotx':np.array(session_state['db']['ra_j2000'],dtype=float), 
                        'ploty':np.array(session_state['db']['dec_j2000'], dtype=float), 
                        'WD':session_state['db']['wd_name'], 
                        'MS':session_state['db']['ms_simbadable_name'], 
                        'WDSpT':session_state['db']['wd_spt'],
                        'Dist':np.array(1000/np.array(session_state['db']['plx'], dtype=float)),
                        'MSG':session_state['db']['ms_gaia_g'],
                        'color': np.array(1000/np.array(session_state['db']['plx'], dtype=float)),
                        'markersize': (1/np.array(session_state['db']['ms_gaia_g'], dtype=float)) * multiplier 
                               })

data=ColumnDataSource(data=datadf)

dist = np.array(1000/np.array(session_state['db']['plx'], dtype=float))


mapper = log_cmap(field_name='color', 
                         palette=Viridis256[::-1],
                         #palette=Turbo256[::-1],
                         low=min(dist), high=max(dist),
                        #low_color=Magma256[150], high_color=Magma256[200]
                        )

tools = "hover, zoom_in, zoom_out, save, undo, redo, pan"
tooltips = [
        ('WD', '@WD'),
        ('MS', '@MS'),
        ('WD SpT', '@WDSpT'),
        ('Dist [pc]','@Dist{0.0}'),
        ('MS Gaia g','@MSG{0.0}')
    ]
p = figure(x_axis_label='RA', y_axis_label='DEC',
        background_fill_color='#222831', border_fill_color='#31363F',outline_line_color='#31363F',
        tools=tools, 
        tooltips=tooltips, toolbar_location="above", width=800, height=400)

p.yaxis.major_label_text_color = "#EEEEEE"
p.yaxis.axis_label_text_color = "#EEEEEE"
p.xaxis.major_label_text_color = "#EEEEEE"
p.xaxis.axis_label_text_color = "#EEEEEE"
p.grid.grid_line_color = '#EEEEEE'

p.scatter('plotx','ploty', source=data, fill_alpha=0.6, size='markersize', 
             line_color=mapper, color=mapper)

color_bar = ColorBar(color_mapper=mapper['transform'], width=8, 
                         location=(0,0), title="Distance",
                        title_text_font_size = '12pt',
                         major_label_text_font_size = '10pt',
                         background_fill_color='#222831',major_label_text_color = "#EEEEEE",
                         title_text_color = "#EEEEEE")
p.add_layout(color_bar, 'right')
st.bokeh_chart(p, use_container_width=True)


############# Visualize data:::::::
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

chart_data['x'] = np.array(session_state['db'][plotx],dtype=float)
chart_data['y'] = np.array(session_state['db'][ploty],dtype=float)
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
data = np.array(session_state['db'][plothist], dtype=float)
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