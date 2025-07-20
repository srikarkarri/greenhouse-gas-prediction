import pandas as pd
import streamlit as st

def set_bg_hack():
  st.markdown(
    f"""
        <style>
        .stApp {{
            background: linear-gradient(to bottom, #e8f5e9, #a5d6a7);  /* Gradient background */
            color: #2e7d32;  /* Green text color */
        }}
        .stButton>button {{
            background-color: #2e7d32;  /* Button green */
            color: white;  /* Button text white */
            border-radius: 8px;
        }}
        .stTextInput, .stNumberInput {{
            border: 1px solid #81c784;
        }}
        </style>
        """,
    unsafe_allow_html=True
  )


set_bg_hack()

st.header("Data")
data_path = '/Users/srikarkarri/PycharmProjects/GreenhouseGas.py/EPA_US_transformed.xlsx - Sheet1.csv'
data = pd.read_csv(data_path)
st.write("View Source Data")
#st.write(data)
st.dataframe(data,use_container_width=True)
@st.cache_data
def convert_df(data):
   return data.to_csv(index=False).encode('utf-8')


csv = convert_df(data)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

view_summary =st.checkbox("View Summary")
if view_summary:
    st.write(data.describe())
col1, col2 = st.columns(2)

with col1:
    column_names =st.checkbox("Column Names")
    if column_names:
        st.write(data.columns)

with col2:
    data_types=st.checkbox("Data Types")
    if data_types:
        st.write(data.dtypes)

col3, col4 = st.columns(2)
with col3:
    pollution_sources=st.checkbox("Pollution Sources")
    if pollution_sources:
        st.write(data["Tier 1 Description"].unique())

with col4:
    pollutant =st.checkbox("Pollutant")
    if pollutant:
        st.write(data["Pollutant"].unique())