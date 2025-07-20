import streamlit as st
import os

st.set_page_config(page_title="Carbon Emission Reduction", page_icon="🌍", layout="centered")

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

# # Define a static background color scheme with even lighter sustainability-themed colors
# st.markdown(
#     """
#     <style>
#         html, body, [data-testid="stAppViewContainer"] {
#             background: linear-gradient(45deg, #E8F5E9, #C8E6C9, #A5D6A7) !important;
#             color: black;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#


#initialize pages

st.sidebar.success('Select a page above.')

#**********************************
import streamlit as st
import pandas as pd
import numpy as np

st.title("Creating a Sustainable Future")
st.text("AI powered app for predicting future greenhouse gas emissions")
st.text("")
st.text("")
st.subheader("Every year, the United States emits nearly 6 billion metric tons of greenhouse gases.")
st.image("/Users/srikarkarri/PycharmProjects/GreenhouseGas.py/venv/background.png", caption="Image taken from ourworldindata.org")
st.text("")

#**********************************

# Sustainability-themed description
st.write("""

Greenhouse gas emissions are a major driver of climate change, contributing to global warming, extreme weather events, 
and public health crises. Accurately predicting future emissions is essential for designing policies to reduce their impact.

Welcome to the emissions prediction tool! This app allows you to predict the amount of carbon emissions (CO2 emissions) 
based on multiple parameters. 

The Problem Statement: Can a machine learning model, specifically an LSTM network, accurately and efficiently predict 
carbon emissions based on the source and state in the USA over the next 5 years to inform and support effective environmental policy and planning?
""")

# Footer
st.write("🌿 Thank you for using the Emission Prediction tool!")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 14px; color: #2d6a4f;">🌍 Together we can reduce emissions and create a sustainable future! 🌍</p>
</div>
""", unsafe_allow_html=True)

# Command to run the Streamlit app
command = "streamlit run Homepage.py"
os.system(command)