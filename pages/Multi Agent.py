import os
from pathlib import Path
import streamlit as st
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import speech_recognition as sr
from matplotlib.textpath import text_to_path
from pydub import AudioSegment
from speech_recognition import Recognizer
from st_audiorec import st_audiorec as audiorec
import io
from openai import OpenAI as Openai
from gtts import gTTS
import pyttsx3
import pydub

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

# Set your OpenAI API key (or use Streamlit secrets/environment variables)
os.environ["OPENAI_API_KEY"] = "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"


### Data Functions ###

@st.cache_data(show_spinner=False)
def load_and_aggregate(csv_path: str, state_filter: str = None):
  """
  Loads the CSV file and aggregates emissions by pollution source.
  Computes the sum of emissions over the next 5 years.
  If state_filter is provided, only data for that state is aggregated.
  Returns an aggregated summary string.
  """
  df = pd.read_csv(csv_path)
  if state_filter:
    # Filter rows where the state matches (case-insensitive)
    df = df[df["state"].str.upper() == state_filter.upper()]

  # Group by pollution source and sum emissions
  agg = df.groupby("pollutions_source", as_index=False)["Emissions"].sum()

  state_text = state_filter.upper() if state_filter else "Nationwide"
  summary_lines = [f"Emissions Summary for {state_text} (Sum over the next 5 years):"]
  for _, row in agg.iterrows():
    summary_lines.append(f"- {row['pollutions_source']}: {row['Emissions']:,.2f} tons")
  summary = "\n".join(summary_lines)
  return summary


@st.cache_data(show_spinner=False)
def load_documents(csv_path: str):
  """
  Loads the CSV file and converts each row into a text document.
  Each row is formatted as:
    "State: {state}, Pollution Source: {pollutions_source}, Year: {Year}, Emissions: {Emissions}"
  The combined text is then split into smaller chunks.
  """
  df = pd.read_csv(csv_path)
  documents = []
  for _, row in df.iterrows():
    doc = (
      f"State: {row['state']}, "
      f"Pollution Source: {row['pollutions_source']}, "
      f"Year: {row['Year']}, "
      f"Emissions: {row['Emissions']}"
    )
    documents.append(doc)
  combined_text = "\n".join(documents)
  splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
  docs = splitter.split_text(combined_text)
  return docs


@st.cache_resource(show_spinner=False)
def get_vectorstore(documents):
  """
  Creates a Chroma vector store from the provided documents using OpenAI embeddings.
  A persistent directory is used to speed up subsequent runs.
  """
  embeddings = OpenAIEmbeddings()
  persist_directory = "chroma_db"
  vectorstore = Chroma.from_texts(documents, embeddings, persist_directory=persist_directory)
  return vectorstore


### Main App ###

def main():
  st.title("Friendly Emissions Assistant")
  assistant = st.selectbox(
    "Please select your assistant",
    ("alloy", "nova", "sage", "shimmer"),
  )
  st.write(
    f"Hi, my name is {assistant}. I am your friendly assistant. I am trained by LSTM model."
    "Ask me any question about emissions trends and insights for your state for the next 5 years"
    "to determine which pollution source has the highest total emissions"
    "and provide recommendations on how to reduce that emission."
  )

  # Optional: Let the user specify a state.
  state = st.text_input("Enter a state code (e.g., CA, FL, TX) [optional]:")

  # Compute aggregated summary (5-year sum) and display it.
  aggregated_summary = load_and_aggregate("predictions.csv", state_filter=state if state else None)
  st.markdown("### Aggregated Emissions Data")
  st.markdown(aggregated_summary)

  # Load raw documents and build vector store.
  documents = load_documents("predictions.csv")
  vectorstore = get_vectorstore(documents)

  # Retrieve additional detailed context based on the query.
  query_text = st.text_input("Enter your question:")
  # voice input using streamlit audiorec
  st.write("Record your question:")
  audio_bytes=audiorec()
  recognized_text = ""
  if audio_bytes:
    st.audio(audio_bytes, format = "audio/wav")
    recognizer = sr.Recognizer()
    try:
      with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
      recognized_text = recognizer.recognize_google(audio_data)
      st.write("You said: ", recognized_text)
    except sr.UnknownValueError:
      st.error("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
      st.error(f"Could not request results from speech recognition service; {e}")
  # Use voice recognized text (if available) otherwise use text input
  query = recognized_text if recognized_text else query_text
  if query:
    with st.spinner("Retrieving data..."):
      retrieved_docs = vectorstore.as_retriever().get_relevant_documents(query)
    retrieved_context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Combine the aggregated summary with the detailed retrieved context.
    combined_context = aggregated_summary + "\n\nDetailed Data:\n" + retrieved_context

    # Define a custom prompt.
    custom_prompt = PromptTemplate(
      input_variables=["context", "question"],
      template="""
You are a friendly assistant for policymakers. Below is the aggregated emissions data (sum over the next 5 years) for various pollution sources, followed by detailed data. Use this combined context to answer the question.

Your answer must:
  - Include the numerical emission values (in tons) for each pollution source.
  - Identify the pollution source with the highest total emissions (this is the focus for the policymaker).
  - Provide insights on emission trends for the specified state (or nationwide if no state is specified).
  - Offer actionable recommendations on how to reduce emissions from the highest pollution source.
  - Use a friendly tone and bullet points (starting with a dash '-') for recommendations.

Combined Context:
{context}

Question:
{question}

Answer:
"""
    )

    # Format the final prompt.
    final_prompt = custom_prompt.format(context=combined_context, question=query)

    # Initialize the LLM.
    llm = OpenAI()
    with st.spinner("Generating answer..."):
      response = llm(final_prompt)

    st.markdown("### Response")
    st.markdown(response)

    # Convert the text response to speech using gTTS
  # response = "Focus on Prescribed Fires."
  # tts = gTTS(text=response, lang='en')
  # audio_fp = io.BytesIO()
  # tts.write_to_fp(audio_fp)
  # audio_fp.seek(0)
    st.markdown("### Voice Response")
    try:
      if response.strip() == "":
        st.error("The response is empty, cannot convert to speech.")
      else:
        client = Openai()
        speech_file_path = Path(__file__).parent / "speech.mp3"
        output = client.audio.speech.create(
          model = "tts-1",
          voice = assistant,
          input = response
        )
        output.stream_to_file(speech_file_path)
        audio_file = open(speech_file_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

    except Exception as e:
      st.error(f"Voice response Error: {e}")


if __name__ == '__main__':
  main()