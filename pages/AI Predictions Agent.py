import pandas as pd
import numpy as np
import os
import streamlit as st
import requests

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

#initialize pages

st.sidebar.success('Select a page above.')

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "ddd7c0c1-a844-4a55-9c8c-7d7d68c5dfb9"
FLOW_ID = "df4372b8-a500-4279-9fd6-6c8924a12efd"
APPLICATION_TOKEN = "AstraCS:cCWZBFbjPZgYMBRZjmKkNfGB:a5bf27067a91442266ffa175ee581cd511d05025327a7c9e6e48aa1b24ac8078"

ENDPOINT = "predict-1"  # The endpoint name of the flow


def run_flow(message: str) -> dict:
  api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

  payload = {
    "input_value": message,
    "output_type": "chat",
    "input_type": "chat",
  }

  headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
  response = requests.post(api_url, json=payload, headers=headers)
  return response.json()


def main():
  st.header("Creating a Sustainable Future")

  st.subheader("AI powered app for predicting future greenhouse gas emissions")
  st.title("Predictions Agent")

  message = st.text_area("Message", placeholder="Ask something...")

  if st.button("Run Flow"):
    if not message.strip():
      st.error("Please enter a message")
      return

    try:
      with st.spinner("Running flow"):
        response = run_flow(message)
      response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
      st.markdown(response)
    except Exception as e:
      st.error(str(e))

  command = "streamlit run main.py"
  os.system(command)

if __name__ == "__main__":
  main()