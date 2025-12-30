import streamlit as st
import ollama
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Kiran T. | AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

# 2. LinkedIn-Style Professional CSS
st.markdown("""
    <style>
    /* Black Skill Tags with White Text */
    .skill-tag {
        background-color: #000000;
        color: #ffffff;
        padding: 6px 15px;
        border-radius: 20px;
        margin: 5px;
        display: inline-block;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Main Chat background */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f3f2ef;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Connection to Mac (Ollama via zrok)
try:
    # It tries to find the URL in Streamlit Secrets (for cloud deployment)
    # If not found, it falls back to a placeholder string
    ZROK_ENDPOINT = st.secrets.get("ZROK_URL", "http://localhost:11434")
    client = ollama.Client(host=ZROK_ENDPOINT)
except Exception:
    st.error("Connection Error: Please check your ZROK_URL in Streamlit Secrets.")

# 4. Sidebar: Profile & Keywords
with st.sidebar:
    try:
        profile_img = Image.open("profile.jpg")
        st.image(profile_img, use_container_width=True)
    except:
        st.warning("📷 profile.jpg not found.")

    st.title("Kiran Kumar Tarlada(Kiran).")
    st.write("🚀 **Solution Architect, Senior SRE & Program Manager**")
    st.write("📍 Greater Seattle Area")
    
    st.divider()
    st.subheader("Core Expertise")
    keywords = ["AWS", "Azure", "Terraform", "SRE", "Disaster Recovery", "Program Management"]
    for kw in keywords:
        st.markdown(f'<div class="skill-tag">{kw}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.caption("🟢 Status: AI Engine Online (M3 Silicon)")

# 5. Main Chat Logic
st.header("📄 Resume Chatbot")
st.write("Ask anything about my professional background, technical skills, or project experience.")

# Load Resume Text
try:
    with open("resume.txt", "r") as f:
        resume_data = f.read()
except FileNotFoundError:
    st.error("Resume content missing! Upload 'resume.txt' to GitHub.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: What projects has Kiran led in Azure?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # SRE-Focused System Instructions
        system_instructions = (
            f"You are a professional assistant for Kiran. Use the following resume: {resume_data}. "
            "Highlight SRE and Program Management skills. Be concise. "
            "If the answer isn't in the text, say 'I'm sorry, that specific detail isn't in the resume.'"
        )

        try:
            # Stream response from your M3 Mac
            response = client.chat(
                model='llama3.2',
                messages=[
                    {'role': 'system', 'content': system_instructions},
                    {'role': 'user', 'content': prompt},
                ],
                stream=True,
            )

            for chunk in response:
                content = chunk['message']['content']
                full_response += content
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Mac Offline: The AI engine is currently unreachable. Error: {e}")
