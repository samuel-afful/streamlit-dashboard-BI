

import streamlit as st
import numpy as np
import pandas as pd



import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='Shop Reports',page_icon=':bar_chart:',layout='wide')



st.title(":bar_chart: Shop Reports and Analysis")
st.markdown('<style>div.block-container{padding-top:2rem}</style>',unsafe_allow_html=True)

f1 = st.file_uploader("Select file to upload", type=(['csv','xls','xlsx']))
if f1 is not None:
    filename = f1.name
    df = pd.read_csv(filename, encoding='ISO-8859-1')
else:
    os.chdir(r"C:\Users\user\Streamlit")
    df = pd.read_csv('Superstore Dataset.csv', encoding='ISO-8859-1')

df['Order Date'] = pd.to_datetime(df['Order Date'])
startDate = df['Order Date'].min()
endDate = df['Order Date'].max()


col1 , col2 = st.columns(2)

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date',startDate))
with col2:
    date2 = pd.to_datetime(st.date_input('End Date',endDate))

df = df[(df['Order Date']>=date1) & (df['Order Date']<=date2)]



# Initialize session state for the selections if they don't already exist
if 'region' not in st.session_state:
    st.session_state['region'] = []
if 'state' not in st.session_state:
    st.session_state['state'] = []
if 'city' not in st.session_state:
    st.session_state['city'] = []



# Sidebar for Region
region_options = sorted(df['Region'].unique())
region_default = [r for r in st.session_state['region'] if r in region_options]
region = st.sidebar.multiselect(
    "Pick Region",
    options=region_options,
    default=region_default
)

# Store the region selection in session state
st.session_state['region'] = region

# Filter DataFrame by selected Region
if region:
    df_filtered = df[df['Region'].isin(region)]
else:
    df_filtered = df.copy()





# Sidebar for State (based on the filtered Region)
state_options = sorted(df_filtered['State'].unique())
state_default = [s for s in st.session_state['state'] if s in state_options]
state = st.sidebar.multiselect(
    "Pick State",
    options=state_options,
    default=state_default
)

# Store the state selection in session state
st.session_state['state'] = state

# Filter DataFrame by selected State
if state:
    df_filtered = df_filtered[df_filtered['State'].isin(state)]

# Sidebar for City (based on the filtered State)
city_options = sorted(df_filtered['City'].unique())
city_default = [c for c in st.session_state['city'] if c in city_options]
city = st.sidebar.multiselect(
    "Pick City",
    options=city_options,
    default=city_default
)

# Store the city selection in session state
st.session_state['city'] = city

# Filter DataFrame by selected City
if city:
    df_filtered = df_filtered[df_filtered['City'].isin(city)]

# Show the final filtered DataFrame
category_df = df_filtered.groupby(df_filtered['Category'], as_index=False)['Sales'].sum()
region_df = df_filtered.groupby(df_filtered['Region'], as_index=False)['Sales'].sum()

#st.dataframe(category_df)
with col1:
  st.subheader('Categorywise Sales')
  fig = px.bar(category_df,x='Category',y='Sales',text = ['${:,.2f}'.format(x) for x in category_df['Sales']])
  st.plotly_chart(fig)


with col2:
  st.subheader('Regionwise Sales')
  fig = px.pie(region_df,values='Sales',names='Region',hole=0.5)
  fig.update_traces(text=region_df['Region'],textposition='outside')
  st.plotly_chart(fig)

cl1,cl2 = st.columns(2)
with cl1:
    with st.expander('Categorical Sales'):
        st.dataframe(category_df.style.background_gradient(cmap='Blues'))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button('Download File',data=csv,file_name='categorical.csv',help='Click here to download CSV file')

with cl2:
    with st.expander('Regional Sales'):
        st.dataframe(region_df.style.background_gradient(cmap='Oranges'))
        csv = region_df.to_csv(index=False).encode('utf-8')
        st.download_button('Download File',data=csv,file_name='regional.csv',help='Click here to download CSV file')


st.subheader('Time Series Of Monthly Sales')
df_filtered['month_year'] = df_filtered['Order Date'].dt.strftime('%Y:%b')

linechart = df_filtered.groupby('month_year')['Sales'].sum().reset_index()
fig = px.line(data_frame=linechart,x='month_year',y='Sales')
st.plotly_chart(fig)


with st.expander('View Data of Time Series'):
    st.write(linechart)


chart1 , chart2 = st.columns(2)

with chart1:
  st.subheader('Regionwise Sales')
  fig = px.pie(df_filtered,values='Sales',names='Segment',template='plotly_dark')
  fig.update_traces(text=df_filtered['Segment'],textposition='inside')
  st.plotly_chart(fig)

with chart2:
  st.subheader('Regionwise Sales')
  fig = px.pie(df_filtered,values='Sales',names='Category',template='gridon')
  fig.update_traces(text=df_filtered['Category'],textposition='inside')
  st.plotly_chart(fig)