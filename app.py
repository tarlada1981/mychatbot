import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Kiran Kumar Tarlada — AI Profile Assistant",
    page_icon="🧠",
    layout="wide"
)

# 2. Setup Groq Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ GROQ_API_KEY missing in Streamlit Secrets.")
    st.stop()

# 3. Custom CSS for "The Modern Dark Hub" Aesthetic
st.markdown("""
    <style>
    /* Global Background and Text */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0c0f;
        color: #e2e8f4;
    }
    [data-testid="stSidebar"] {
        background-color: #111418;
        border-right: 1px solid #1f2530;
    }
    
    /* Headers & Text */
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
        color: #ffffff;
    }
    
    /* Custom Skill Tags */
    .skill-tag {
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 4px;
        background: #181c22;
        border: 1px solid #1f2530;
        color: #6b7a96;
        font-family: monospace;
        display: inline-block;
        margin: 3px;
        transition: all 0.2s;
    }
    .skill-tag:hover {
        border-color: #4f8ef7;
        color: #7eb8f7;
    }

    /* Message Bubbles */
    .stChatMessage {
        background-color: transparent !important;
        padding: 1rem 0;
    }
    
    /* User Bubble */
    [data-testid="stChatMessage"]:nth-child(even) {
        flex-direction: row-reverse;
        text-align: right;
    }
    
    .stChatMessage [data-testid="stMarkdownContainer"] {
        background: #131720;
        border: 1px solid #1f2530;
        border-radius: 12px;
        padding: 15px;
        color: #e2e8f4;
        line-height: 1.6;
    }

    /* Style the Chat Input */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: transparent !important;
    }
    
    /* Horizontal Divider */
    hr {
        border-color: #1f2530;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar: Profile & Model Selection
with st.sidebar:
    # Avatar Circle
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 20px;">
            <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #1a2d5a 0%, #0f1c3a 100%); 
            border: 2px solid #4f8ef7; display: flex; align-items: center; justify-content: center; font-size: 28px; color: #7eb8f7; 
            box-shadow: 0 0 20px rgba(79,142,247,0.15);">KK</div>
            <h2 style="margin-top:15px; font-size: 18px;">Kiran Kumar Tarlada</h2>
            <p style="color: #c9a84c; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">Principal Architect</p>
            <p style="color: #6b7a96; font-size: 12px;">📍 Hyderabad, India</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    st.markdown("<p style='font-size:10px; color:#6b7a96; text-transform:uppercase;'>Core Skills</p>", unsafe_allow_html=True)
    skills = ["AWS", "Azure", "SRE", "Terraform", "FinOps", "RAG / AI", "Kubernetes", "CI/CD"]
    skill_html = "".join([f'<div class="skill-tag">{s}</div>' for s in skills])
    st.markdown(skill_html, unsafe_allow_html=True)
    
    st.divider()
    
    # Model Config
    model_options = {
        "Llama 3.3 70B (Versatile)": "llama-3.3-70b-versatile",
        "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant"
    }
    selected_model = st.selectbox("AI Brain Selection:", options=list(model_options.keys()))
    model_id = model_options[selected_model]

# 5. Main Layout
col_chat, col_visuals = st.columns([3, 1], gap="large")

with col_chat:
    st.markdown("### 🧠 Profile AI Assistant")
    st.markdown("<p style='color:#6b7a96; font-size:13px; margin-top:-15px;'>Ask about 20 years of Cloud & SRE expertise</p>", unsafe_allow_html=True)
    
    # Load Resume Data
    try:
        with open("resume.txt", "r") as f:
            resume_data = f.read()
    except FileNotFoundError:
        st.error("resume.txt not found. Please upload it to the root directory.")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I'm Kiran's AI profile partner. Ask me about his work with AWS migrations, FinOps, or Azure DR strategies."}
        ]

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("How has Kiran optimized cloud costs?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing Professional History..."):
                try:
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[
                            {"role": "system", "content": f"You are a professional assistant for Kiran. Use this resume: {resume_data}. Be concise and use bullet points for lists."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    ai_content = response.choices[0].message.content
                    st.markdown(ai_content)
                    st.session_state.messages.append({"role": "assistant", "content": ai_content})
                except Exception as e:
                    st.error(f"Error: {e}")

# 6. Right Column: Featured Projects/Visuals
with col_visuals:
    st.markdown("### Featured")
    
    visuals = [
        {"file": "Azure.png", "cap": "Cloud DR Design"},
        {"file": "sre.gif", "cap": "SRE & Reliability"},
        {"file": "aws.gif", "cap": "AWS Infrastructure"}
    ]
    
    for v in visuals:
        try:
            st.image(v["file"], caption=v["cap"], use_container_width=True)
        except:
            st.caption(f"Ref: {v['cap']}")
        st.divider()
