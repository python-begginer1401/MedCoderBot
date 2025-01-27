

import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from gtts import gTTS
from io import BytesIO
import textwrap


# Initialize Google Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Sidebar for API Key input and tab selection
with st.sidebar:
    tabs = st.sidebar.radio("Services/Programs", ["🏠 Home", "💬 MedCoderBot" ])


    api_key = st.text_input("Google API Key", key="geminikey", type="password")

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)


# Main Page Tab
if tabs == "🏠 Home":
    st.title("🙊 MedCoderBot ")
    st.write("""
        Welcome to 💬 MedCoderBot!
        just upload the pateint's file and I'll give you the medical code to it!!
        Select a tab from the sidebar to get started!
    """)
# Chatbot Tab
elif tabs == "💬 MedCoderBot":
    st.title("💬 MedCoderBot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    prompt = st.chat_input("Type a message...")
    if prompt and api_key:
        genai.configure(api_key=api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        prompt_text = f"SYSTEM: Engage in a helpful conversation with the user, considering they have Global Developmental Delay.\nUSER: {prompt}"
        response = model.generate_content(prompt_text).text
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
