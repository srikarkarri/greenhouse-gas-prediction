import pickle
import streamlit as st
import os

st.set_page_config(page_title="Emission Prediction by State and Source", page_icon="🌍", layout="centered")

with open('/Users/srikarkarri/PycharmProjects/GreenhouseGas.py/masterDictionary', 'rb') as file:
  master_dict = pickle.load(file)

print(master_dict)


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

# Title with environmental icon
st.markdown("<h1 style='text-align: center; color: #2d6a4f;'>🌿 Emissions Prediction for Sustainability by State and Source 🌿</h1>", unsafe_allow_html=True)

year = st.number_input("Enter the year:", step = 1)
state = st.number_input("Enter the state FIPS:", step = 1)
tier1 = st.number_input("Enter the Tier 1 Code:", step = 1)

# Predict emissions
if st.button("Predict Emissions"):
  data_year_form = master_dict[f'{state}_{tier1}']
  emissions = data_year_form[int(year)]
  st.metric(label="Emissions", value=emissions)

# Footer
st.write("🌿 Thank you for using the Emission Prediction tool!")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 14px; color: #2d6a4f;">🌍 Together we can reduce emissions and create a sustainable future! 🌍</p>
</div>
""", unsafe_allow_html=True)

# Command to run the Streamlit app
command = "streamlit run Predict_Emissions_by_State_and_Source.py"
os.system(command)