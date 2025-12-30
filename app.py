import streamlit as st
from groq import Groq
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Kiran T. | AI Portfolio", page_icon="🚀", layout="wide")

# 2. Setup Groq Client (Pulling from Secrets)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets!")
    st.stop()

# 3. Professional Styling
st.markdown("""
    <style>
    .skill-tag {
        background-color: #0077b5; color: white; border-radius: 20px;
        padding: 5px 15px; margin: 4px; display: inline-block; font-size: 13px;
    }
    .stChatMessage { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar: Profile
with st.sidebar:
    try:
        st.image("profile.jpg", use_container_width=True)
    except:
        st.info("Upload profile.jpg to GitHub to see your photo.")
    
    st.title("Kiran Kumar Tarlada.")
    st.write("Senior SRE & Program Manager")
    st.divider()
    st.subheader("Skills")
    for s in ["AWS", "Azure", "Terraform", "SRE", "Kubernetes"]:
        st.markdown(f'<div class="skill-tag">{s}</div>', unsafe_allow_html=True)
    st.divider()
    st.caption("⚡ Powered by Groq (Llama 3.2 11B)")

# 5. Main Logic
st.header("📄 AI Career Assistant")

# Load Resume
try:
    with open("resume.txt", "r") as f:
        resume_content = f.read()
except FileNotFoundError:
    st.error("resume.txt not found in GitHub repository.")
    st.stop()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask about Kiran's experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # System instructions to keep the bot focused on your resume
        system_prompt = f"You are a helpful assistant for Kiran. Answer questions using this resume: {resume_content}"
        
        try:
            # Groq Cloud Inference
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview", # High-performance free-tier model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            # Use Streamlit's built-in streaming display
            full_response = st.write_stream(completion)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Cloud Inference Error: {e}")
