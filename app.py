import streamlit as st
import ollama
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Professional AI Portfolio", layout="wide")

# Custom CSS for LinkedIn-style Blue accents
st.markdown("""
    <style>
    .skill-tag {
        background-color: #0077b5;
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        margin: 5px;
        display: inline-block;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Profile Section
with st.sidebar:
    try:
        image = Image.open("profile.jpg")
        st.image(image, use_container_width=True)
    except:
        st.warning("Place 'profile.jpg' in the folder to see your photo.")
    
    st.title("Kiran Kumar Tarlada(Kiran)")
    st.write("🚀 **Solution Arcitect, Senior SRE & Program Manager**")
    st.write("📍 Hyderabad, India")
    st.divider()
    
    st.subheader("Skills & Expertise")
    keywords = ["AWS", "Azure", "Terraform", "SRE", "Disaster Recovery", "Program Management"]
    for kw in keywords:
        st.markdown(f'<div class="skill-tag">{kw}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.info("This AI is trained on my specific resume and project history.")

# 3. Main Chat Interface
st.header("📄 Resume Insights Chatbot")
st.caption("Ask me about my experience with cloud migrations, SRE practices, or project leadership.")

# Load Resume Content
try:
    with open("resume.txt", "r") as f:
        resume_context = f.read()
except FileNotFoundError:
    st.error("Error: 'resume.txt' not found.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ex: 'Tell me about your experience with Terraform'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response from Ollama
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        system_msg = (
            f"You are a professional recruiting assistant for the candidate described here: {resume_context}. "
            "Answer questions based on the resume. Be professional, concise, and emphasize the candidate's strengths."
        )
        
        response = ollama.chat(
            model='llama3.2', # Ensure you have this model pulled
            messages=[
                {'role': 'system', 'content': system_msg},
                {'role': 'user', 'content': prompt}
            ],
            stream=True,
        )

        for chunk in response:
            content = chunk['message']['content']
            full_response += content
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
