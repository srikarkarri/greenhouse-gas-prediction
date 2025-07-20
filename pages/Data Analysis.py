import pandas as pd
import streamlit as st
import pickle

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

st.header("Data Analysis and Visualization")
data_path = '/Users/srikarkarri/PycharmProjects/GreenhouseGas.py/EPA_US_transformed.xlsx - Sheet1.csv'
data = pd.read_csv(data_path)
group_by_state =data.groupby('State').sum().reset_index().copy()
group_by_source = data.groupby('Tier 1 Description').sum().reset_index().copy()
group_by_state_source = data.groupby(['State','Tier 1 Description','Year']).sum().reset_index().copy()
group_by_state_year = data.groupby(['State','Year']).sum().reset_index().copy()
#group_by_state_year_texas =group_by_state_year[group_by_state_year['State'].isin(['California','Florida','Texas'])]
group_by_year_source = data.groupby(['Tier 1 Description','Year']).sum().reset_index().copy()

st.write("Emissions by State")
st.bar_chart(group_by_state,x="State",y="Emissions")

#st.write("Yearly Emissions Trend by State")
#st.line_chart(group_by_state_year,x="Year",y="Emissions",color ="State")

st.write("Emissions by Pollution Sources")
st.bar_chart(group_by_source,x="Tier 1 Description",y="Emissions")

st.write("Yearly Emissions Trend by Pollution Sources")
st.line_chart(group_by_year_source,x="Year",y="Emissions",color ="Tier 1 Description")


tab1, tab2, tab3 = st.tabs(["Emissions by State", "Emissions by Pollution Sources","Yearly Emissions Trend by Pollution Sources"])
with tab1:
    st.bar_chart(group_by_state,x="State",y="Emissions")
with tab2:
    st.bar_chart(group_by_source,x="Tier 1 Description",y="Emissions")
with tab3:
    st.line_chart(group_by_year_source,x="Year",y="Emissions", color="Tier 1 Description")