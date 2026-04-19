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
    st.write("🚀 **20+ years designing fault-tolerant, highly available architectures across AWS and Azure. Specialising in zero-trust security, SRE adoption, platform modernisation, and cost optimisation for global enterprises.**")
    
    # --- FIXED: Indented properly to stay inside the sidebar ---
    st.subheader("🌐 Explore My Work")
    portfolio_url = "https://tarlada1981.github.io/Cloudarchitect/"
    link_text = "Click here to visit my detailed portfolio"
    same_window_link = f'<a href="{portfolio_url}" target="_self" style="text-decoration:none; font-weight:bold; color:#0077b5;">{link_text}</a>'
    st.markdown(same_window_link, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🛠️ Core Competencies")
    skills = ["Datacenter Consolidations","Cloud (AWS/Azure)", "SRE", "Terraform", "Kubernetes", "Automation"]
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

# --- LEFT COLUMN: Chat Interface ---
with col_chat:
    st.header("📄 AI Resume Assistant")
    
    try:
        with open("resume.txt", "r") as f:
            resume_data = f.read()
    except FileNotFoundError:
        st.error("resume.txt not found.")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if prompt := st.chat_input("Ask about Kiran's experience..."):
        st.session_state.messages.insert(0, {"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": f"You are a professional assistant for Kiran. Use this resume: {resume_data}"},
                        {"role": "user", "content": prompt}
                    ],
                    stream=False 
                )
                ai_content = response.choices[0].message.content
                st.session_state.messages.insert(1, {"role": "assistant", "content": ai_content})
            except Exception as e:
                st.error(f"Inference Error: {e}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- RIGHT COLUMN: GIFs ---
with col_visuals:
    st.write("### Projects")
    try:
        st.image("Azure.png", caption="Site Reliability Engineering", use_container_width=True)
    except:
        st.caption("⚠️ sre.gif not found")
        
    st.divider()
    try:
        st.image("sre.gif", caption="Site Reliability Engineering", use_container_width=True)
    except:
        st.caption("⚠️ sre.gif not found")
        
    st.divider()
    
    try:
        st.image("aws.gif", caption="AWS Infrastructure", use_container_width=True)
    except:
        st.caption("⚠️ aws.gif not found")
    
    st.divider() # Added a divider for visual consistency
    
    
