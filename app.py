import streamlit as st
# streamlit: web based app making
# light python framework

st.title("AI resume maker")
st.markdown("""## user can create or
 download
AI created resume based
 on high ATS score""")


#============Agent code===============
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
 

# ================API key load================
GOOGLE_API_KEY=st.sidebar.text_input("GOOGLE_API_KEY",TYPE="password")
GROQ_API_KEY=st.sidebar.text_input("GROQ_API_KEY",TYPE="password")
TAVILI_API_KEY=st.sidebar.text_input("TAVILI_API_KEY",TYPE="password")

# =======================model building===================================
model= ChatGoogleGenerativeAI(
    model='gemini-3.5-flash-lite',
    google_api_key=GOOGLE_API_KEY
)
# tool
def search_recent_new_jobs(query):
  """this function helps to search recent news or recent jobs
  related to given search query suppose user write python developer jobs
  it should return trending news and jobs link"""
  client=TavilyClient(
  api_key=TAVILY_API_KEY
  )
  return client.search(query)

# agent creation
from langchain.agents import create_agent
agent=create_agent(
    model=model,
    tools=[search_recent_new_jobs]
)

#===========Prompt generator=======================================
def prompt_generator(agent=agent):
  """this function help to give detailed prompt
  followed by chain of thoughts and
  persona based prompting, main task
  is to give detailed prompt to build resume for students
  or experienced job seekers based on their personal
  information."""
  prompt="""you are a senior HR resume analyzer main task
  is to give detailed prompt to build resume for students
  or experienced job seekers based on their personal
  information.system instructions i want model to generate resume
  in HTML format include that in prompt
  """
  response=agent.invoke(prompt)
  file_name='prompt.py'
  with open(file_name,'w') as f:
    f.write(response.content[-1]['text'])
  return "prompt file generated successfully,agent can read me"
prompt_generator(model)
       
# tool 2:
def Resume_maker_prompt():
  """this function just gives updated prompt
  for the model"""
  with open('prompt.py','r') as f:
    prompt=f.read()
  return prompt
Resume_maker_prompt()
# ====================Generate Resume=================
prompt="""you are a helpful AI assistant
with job resume maker,your task is to give,
HTML format resume,with proper designing using recent CSS andJS
code,with professional design format.
user will upload data and return HTML format resume
always use different styling"""

final_prompt=prompt+Resume_maker_prompt()

user_details="""user details:given below:give python developer resume
"""
query=user_details+final_prompt

if st.button("Generate Resume"):
  with st.spinner("Running Agent...."):
    
    response=agent.invoke({'messages':[{'role':'user',
    "content":query}]})
    code=response['messages'][-1].content[-1]['text']

    # st.markdown(code)
    st.html(code,width="strech",unsafe_allow_javascript=True)


