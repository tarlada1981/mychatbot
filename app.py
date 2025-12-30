import streamlit as st
from groq import Groq
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Kiran T. | AI Career Partner", 
    page_icon="🤖", 
    layout="wide"
)

# 2. Setup Groq Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ GROQ_API_KEY missing in Streamlit Secrets.")
    st.stop()

# 3. Professional Styling
st.markdown("""
    <style>
    .skill-tag {
        background-color: #e8f3ff;
        color: #0077b5;
        padding: 5px 12px;
        border-radius: 15px;
        margin: 3px;
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #0077b5;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar: Profile & Skills
with st.sidebar:
    try:
        st.image("profile.jpg", use_container_width=True)
    except:
        st.info("📷 profile.jpg not found.")
    
    st.title("Kiran Kumar Tarlada.")
    st.write("🚀 **Solution Architect, Senior SRE & Program Manager**")
    
    st.divider()
    st.subheader("🛠️ Core Competencies")
    skills = ["SRE / DevOps", "Cloud (AWS/Azure)", "Terraform", "Kubernetes", "Automation"]
    for skill in skills:
        st.markdown(f'<div class="skill-tag">{skill}</div>', unsafe_allow_html=True)
    
    st.divider()
    model_options = {
        "Llama 3.3 70B": "llama-3.3-70b-versatile",
        "Llama 3.1 8B": "llama-3.1-8b-instant"
    }
    selected_model = st.selectbox("AI Brain:", options=list(model_options.keys()))
    model_id = model_options[selected_model]

# 5. Main Layout Columns
col_chat, col_visuals = st.columns([3, 1], gap="large")

# --- LEFT COLUMN: Chat Interface (Modified for Top-Down) ---
with col_chat:
    st.header("📄 AI Resume Assistant")
    
    # Load Resume
    try:
        with open("resume.txt", "r") as f:
            resume_data = f.read()
    except FileNotFoundError:
        st.error("resume.txt not found.")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- INPUT AT THE TOP ---
    if prompt := st.chat_input("Ask about Kiran's experience..."):
        # Insert User Message at the TOP of the history
        st.session_state.messages.insert(0, {"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            try:
                # Get response from Groq
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": f"You are a professional assistant for Kiran. Use this resume: {resume_data}"},
                        {"role": "user", "content": prompt}
                    ],
                    stream=False # Stream=False works best for prepending content to prevent UI flicker
                )
                ai_content = response.choices[0].message.content
                # Insert Assistant Message at the TOP (index 1, below the user message)
                st.session_state.messages.insert(1, {"role": "assistant", "content": ai_content})
            except Exception as e:
                st.error(f"Inference Error: {e}")

    # --- DISPLAY MESSAGES (History now shows newest first) ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- RIGHT COLUMN: GIFs ---
with col_visuals:
    st.write("### Projects")
    try:
        st.image("sre.gif", caption="Site Reliability Engineering", use_container_width=True)
    except:
        st.caption("⚠️ sre.gif not found")
        
    st.divider()
    
    try:
        st.image("aws.gif", caption="Cloud Infrastructure", use_container_width=True)
    except:
        st.caption("⚠️ aws.gif not found")
