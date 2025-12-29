import streamlit as st
from ollama import Client
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kiran's AI Portfolio", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .skill-tag {
        background-color: #0077b5; color: white; border-radius: 15px;
        padding: 5px 12px; margin: 4px; display: inline-block; font-size: 13px;
    }
    .stChatMessage { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIG: YOUR ZROK URL ---
# Note: For security, you can move this to Streamlit Secrets later
ZROK_URL = "https://3ikiu6yq8kt3.share.zrok.io" 
client = Client(host=ZROK_URL)

# --- SIDEBAR: LinkedIn Style ---
with st.sidebar:
    try:
        st.image("profile.jpg", use_container_width=True)
    except:
        st.info("Upload 'profile.jpg' to show your photo.")
        
    st.title("Kiran T.")
    st.write("🚀 **Senior SRE & Program Manager**")
    st.write("☁️ AWS | Azure | Terraform")
    
    st.divider()
    st.subheader("Core Expertise")
    skills = ["AWS", "Azure", "Terraform", "SRE", "Disaster Recovery", "Program Management"]
    for s in skills:
        st.markdown(f'<div class="skill-tag">{s}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.caption("AI powered by Llama 3.2 on local M3 Silicon via secure zrok tunnel.")

# --- MAIN INTERFACE ---
st.header("📄 Career Assistant")

# Load Resume context
try:
    with open("resume.txt", "r") as f:
        resume_content = f.read()
except FileNotFoundError:
    st.error("Missing 'resume.txt'. Please add it to the project folder.")
    st.stop()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask me about Kiran's experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # System instructions
        system_prompt = f"You are an assistant for Kiran. Answer using this resume ONLY: {resume_content}"
        
        try:
            # Note: We use the 'client' we created above with the ZROK_URL
            response = client.chat(
                model='llama3.2',
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                stream=True
            )
            for chunk in response:
                full_response += chunk['message']['content']
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Mac Offline: Ensure 'zrok share' is running on your MacBook. ({e})")
