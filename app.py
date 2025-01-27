import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import textwrap

st.set_page_config(page_title='MedCoderBot', page_icon=':robot_face:', layout='wide')

# Initialize Google Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Sidebar for API Key input and tab selection
with st.sidebar:
    tabs = st.sidebar.radio("Services/Programs", ["🏠 Home", "💬 MedCoderBot"])

    api_key = st.text_input("Google API Key", key="geminikey", type="password")

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Main Page Tab
if tabs == "🏠 Home":
    st.title("🙊 MedCoderBot")
    st.write("""
        Welcome to 💬 MedCoderBot!
        Just upload the patient's file and I'll give you the medical code for it!
       
        Select a tab from the sidebar to get started!
    """)

# Chatbot Tab
elif tabs == "💬 MedCoderBot":
    st.title("💬 MedCoderBot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # File upload feature
    uploaded_file = st.file_uploader("Upload the patient's file (e.g., text, PDF, etc.)", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        file_content = uploaded_file.read()
        st.write("File uploaded successfully!")
        st.text_area("File Content Preview", file_content.decode("utf-8") if uploaded_file.type == "text/plain" else "File preview not available for this format.", height=150)

    # Chat input
    prompt = st.chat_input("Type a message...")
    if prompt and api_key:
        genai.configure(api_key=api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        prompt_text = f"SYSTEM: You are a medical coder code based on the ICD 10 system with achi \nUSER: {prompt}"
        response = model.generate_content(prompt_text).text
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
