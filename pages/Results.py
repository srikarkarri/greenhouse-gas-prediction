import pandas as pd
import streamlit as st
import pickle
import plotly.express as px

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

st.title("Results")

st.write("RMSE heatmap")
with open('/Users/srikarkarri/PycharmProjects/GreenhouseGas.py/rmses', 'rb') as file:
  rmses = pickle.load(file)

data = [[0.03, 0.05, 0.17, 0.13], [0.04, 0.02, 0.14, 0.20], [0.04, 0.04, 0.10, 0.23]]
df= pd.DataFrame(data,index=['CA','FL','TX'],columns =['Highway Vehicles','Offhighway','Wild Fires',"Prescribed Fires"])
fig = px.imshow(df, labels=dict(x='Pollution Sources',y='State',color="RMSE"),x=df.columns, y=df.index,text_auto=True, aspect="auto")

st.plotly_chart(fig, theme="streamlit")

pred_data=pd.read_csv("/Users/srikarkarri/PycharmProjects/GreenhouseGas.py/Emission_predictions.csv")
state_unscaled = st.selectbox("Please select the state", ('TX','CA','FL'))
select_data = pred_data.loc[pred_data['State'] == state_unscaled]
st.bar_chart(select_data,x="Pollution Source",y="Emissions Over Next 5 years")